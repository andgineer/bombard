import json
import logging
from typing import Any, Dict, List, Optional, Set, Union
from urllib.parse import urlparse

from bombard import request_logging
from bombard.attr_dict import AttrDict
from bombard.http_request import EXCEPTION_STATUS, http_request
from bombard.pretty_ns import time_ns
from bombard.pretty_sz import pretty_sz
from bombard.report import Reporter
from bombard.show_descr import markdown_for_terminal
from bombard.terminal_colours import dark_red, green, red
from bombard.weaver_mill import WeaverMill

log = logging.getLogger()

DEFAULT_OK = {200}
DEFAULT_OVERLOAD = [502, 504]
PREPARE = "prepare"
AMMO = "ammo"


def apply_supply(s: str, supply: Dict[str, Any]) -> str:
    # todo: add args
    if not isinstance(s, str):
        return s
    try:
        return str(eval(f'f"""{s}"""', supply))  # pylint: disable=eval-used
    except Exception as e:
        log.error(f'Cannot eval "{s}":\n{e}', exc_info=True)
    return s


def apply_supply_dict(request: Dict[str, Any], supply: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use supply to substitute all {name} in request strings.
    """
    for name, value in request.items():
        if isinstance(request[name], dict):
            request[name] = apply_supply_dict(request[name], supply)
        elif isinstance(value, str):
            request[name] = apply_supply(request[name], supply)
    return request


class Bombardier(WeaverMill):  # pylint: disable=too-many-instance-attributes
    """
    Use horde of threads to make HTTP-requests
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        args: Any,
        campaign_book: Dict[str, Any],
        supply: Optional[Dict[str, Any]] = None,
        ok_statuses: Optional[Set[int]] = None,
        overload_statuses: Optional[List[int]] = None,
    ):
        self.supply = supply if supply is not None else {}
        self.supply["args"] = args
        self.args = args
        self.campaign = campaign_book
        self.ok = ok_statuses if ok_statuses is not None else DEFAULT_OK
        self.overload = overload_statuses if overload_statuses is not None else DEFAULT_OVERLOAD
        self.request_fired = False  # from any request reload() was called
        self.resp_count = 0

        self.show_request = {1: "Sent 1st request.."}
        self.show_response = {1: "Got 1st response.."}
        self.reporter = Reporter(
            time_units=("ms" if args.ms else None),
            time_threshold_ms=int(args.threshold),
            success_statuses=self.ok,
        )
        request_logging.pretty_ns = self.reporter.pretty_ns

        super().__init__(args.threads)

    def status_coloured(self, status: Union[str, int]) -> str:
        """
        Paint ok status as green and overload as red using terminal control codes.

        If status has special string value (EXCEPTION_STATUS) paint it red.
        """
        if status in self.ok:
            return green(str(status))
        if status in self.overload or status == EXCEPTION_STATUS:
            return dark_red(str(status))
        return red(str(status))

    @staticmethod
    def get_headers(request: Dict[str, Any], body_is_json: bool) -> Dict[str, Any]:
        """
        Treat special value 'json' as Content-Type: application/json
        """
        predefined = {
            "json": {"Content-Type": "application/json"},
        }
        if "headers" in request and isinstance(request["headers"], str):
            # headers in request description just a string: this should be some predefined code
            for known, value in predefined.items():
                if request["headers"].lower() == known:
                    return value
        result = {}
        for name, val in request.get("headers", {}).items():
            for known, value in predefined.items():
                if name.lower() == known:
                    result.update(value)
                    break
            else:
                result.update({name: val})
        if body_is_json and "Content-Type" not in result:
            result.update(predefined["json"])
        return result

    def process_resp(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        ammo: Dict[str, Any],
        status: Union[int, str],
        resp: str,
        elapsed: int,
        size: int,
    ) -> None:
        request = ammo["request"]
        self.reporter.log(status, elapsed, request.get("name"), size)
        if status in self.ok:
            log.debug(f"{status} reply\n{resp}")
            if "extract" in request:
                try:
                    data = json.loads(resp)
                    if not hasattr(request["extract"], "items"):
                        request["extract"] = {request["extract"]: request["extract"]}
                    for name, extractor in request["extract"].items():
                        if not extractor:
                            extractor = name
                        if "[" in extractor:
                            self.supply[name] = eval(  # pylint: disable=eval-used
                                f"data{extractor}"
                            )
                        else:
                            self.supply[name] = data[extractor]
                except Exception as e:
                    log.error(
                        f"Cannot extract {request['extract']} from {resp}:\n{e}",
                        exc_info=True,
                    )
            if "script" in request:
                supply = None
                try:
                    # Supply immediately repeats all changes in the self.supply
                    # so if the script spawns new requests they already get new values
                    supply = AttrDict(self.supply, **ammo["supply"])
                    context = {
                        "reload": self.reload,
                        "resp": json.loads(resp),
                        "args": self.args,
                        "supply": supply,
                        "ammo": AttrDict(self.campaign[AMMO]),
                    }
                    if "compiled" not in request:
                        request["compiled"] = compile(request["script"], "script", "exec")
                    exec(request["compiled"], context)  # pylint: disable=exec-used
                except Exception as e:
                    log.error(
                        f"Script fail\n{e}\n\n{request['script']}\n\n{supply}\n",
                        exc_info=True,
                    )

    @staticmethod
    def beautify_url(
        url: str,
        method: str,
        body: Optional[str],  # pylint: disable=unused-argument
    ) -> str:  # pylint: disable=unused-argument
        urlparts = urlparse(url)
        path = urlparts.path if len(urlparts.path) < 15 else f"...{urlparts.path[-15:]}"
        query = f"?{urlparts.query}" if urlparts.query else ""
        if urlparts.fragment:
            query += f"#{urlparts.fragment}"
        query = query if len(query) < 15 else f"?...{query[-15:]}"
        return f"""{method} {urlparts.netloc}{path}{query}"""

    def worker(self, thread_id: int, job: Dict[str, Any]) -> None:
        """
        Thread callable.
        Strike ammo from queue.
        """
        try:
            # setup logging ASAP and as safe as possible
            if isinstance(job, dict):
                request = job.get("request", {})
                ammo_id = job.get("id", "")
                ammo_name = request.get("name", "")
            else:
                request = {}
                ammo_id = None
                ammo_name = None
            request_logging.sending(thread_id, ammo_id, ammo_name)
            pretty_url = ""  # we use it in `except`
            try:
                job = apply_supply_dict(job, dict(self.supply, **job["supply"]))

                url = request.get("url", "")
                method = request["method"] if "method" in request else "GET"
                body = json.dumps(request["body"]) if "body" in request else None
                headers = self.get_headers(request, body is not None)
                pretty_url = self.beautify_url(url, method, body)

                log.debug(  # pylint: disable=logging-not-lazy
                    f"Bomb to drop:\n{pretty_url}" + ("\n{body}" if body is not None else "")
                )
                if self.args.quiet and ammo_id in self.show_request:
                    print(f"{self.show_request[ammo_id].format(id=ammo_id):>15}\r", end="")
                log.info(pretty_url)

                start_ns = time_ns()
                status: Union[str, int]
                if self.args.dry:
                    status, resp = list(self.ok)[0], json.dumps(request.get("dry"))
                else:
                    status, resp = http_request(url, method, headers, body, self.args.timeout)

                request_logging.receiving()

                self.process_resp(job, status, resp, time_ns() - start_ns, len(resp))

                self.resp_count += 1
                if self.args.quiet and self.resp_count in self.show_response:
                    print(
                        f"{self.show_response[self.resp_count].format(id=self.resp_count):>15}\r",
                        end="",
                    )
                log.info(
                    self.status_coloured(status)
                    + f" ({pretty_sz(len(resp))}) "
                    + pretty_url
                    + " "
                    + (red(resp) if status == EXCEPTION_STATUS else "")
                )
            except Exception as e:
                log.info(  # pylint: disable=logging-not-lazy
                    f"{pretty_url} {red(str(e))}", exc_info=True
                )
        finally:
            request_logging.main_thread()

    def reload(
        self,
        requests: Any,
        repeat: Optional[int] = None,
        prepare: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Add request(s) to the bombardier queue `repeat`-times (args.repeat if None).
        If `repeat` field exists in the request additionally repeats as defined by it.

        Requests can be one request or list of requests.
        If supply specified it'll be used in addition to self.supply.

        Arg `prepare` indicate call from main, not from request script.
        So we know if any scripts call reload (self.request_fired)
        """
        if not prepare:
            self.request_fired = True
        if not isinstance(requests, list):
            requests = [requests]
        if repeat is None:
            repeat = self.args.repeat
        for request in requests:
            try:
                _repeat = int(apply_supply(request["repeat"], self.supply))
            except (ValueError, KeyError):
                _repeat = repeat
            for _ in range(_repeat):
                self.job_count += 1
                if (
                    self.job_count % self.args.threads == 0
                    or self.job_count < self.args.threads
                    and self.job_count % 10 == 0
                ):
                    # show each 10th response before queue is full and then each time it's full
                    self.show_response[self.job_count] = f"Got {self.job_count} responses..."
                self.put({"id": self.job_count, "request": request, "supply": kwargs})

    def report(self) -> None:
        log.warning(  # pylint: disable=logging-not-lazy
            "\n" + "=" * 100 + "\n" + markdown_for_terminal(self.reporter.report()) + "=" * 100 + "\n"
        )
