import json
import logging
from typing import Any
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


def apply_supply(s: str, supply: dict[str, Any]) -> str:
    # todo: add args
    if not isinstance(s, str):
        return s
    try:
        return str(eval(f'f"""{s}"""', supply))  # noqa: S307
    except Exception:  # noqa: BLE001
        log.exception(f'Cannot eval "{s}"')
    return s


def apply_supply_dict(request: dict[str, Any], supply: dict[str, Any]) -> dict[str, Any]:
    """
    Use supply to substitute all {name} in request strings.
    """
    for name, value in request.items():
        if isinstance(value, dict):
            request[name] = apply_supply_dict(request[name], supply)
        elif isinstance(value, str):
            request[name] = apply_supply(request[name], supply)
    return request


class Bombardier(WeaverMill):
    """
    Use horde of threads to make HTTP-requests
    """

    def __init__(
        self,
        args: Any,
        campaign_book: dict[str, Any],
        supply: dict[str, Any] | None = None,
        ok_statuses: set[int] | None = None,
        overload_statuses: list[int] | None = None,
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

    def status_coloured(self, status: str | int) -> str:
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
    def get_headers(request: dict[str, Any], body_is_json: bool) -> dict[str, Any]:
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
                result[name] = val
        if body_is_json and "Content-Type" not in result:
            result.update(predefined["json"])
        return result

    def process_resp(
        self,
        ammo: dict[str, Any],
        status: int | str,
        resp: str,
        elapsed: int,
        size: int,
    ) -> None:
        request = ammo["request"]
        self.reporter.log(status, elapsed, request.get("name"), size)

        if status not in self.ok:
            return

        log.debug(f"{status} reply\n{resp}")

        if "extract" in request:
            self._handle_extraction(request, resp)

        if "script" in request:
            self._execute_script(request, ammo, resp)

    def _handle_extraction(self, request, resp):
        try:
            data = json.loads(resp)
            if not hasattr(request["extract"], "items"):
                request["extract"] = {request["extract"]: request["extract"]}

            for name, extract_key in request["extract"].items():
                extractor = extract_key or name
                self._extract_value(data, name, extractor)

        except Exception:
            log.exception(
                f"Cannot extract {request['extract']} from {resp}",
            )

    def _extract_value(self, data, name, extractor):
        if "[" in extractor:
            self.supply[name] = eval(f"data{extractor}")  # noqa: S307
        else:
            self.supply[name] = data[extractor]

    def _execute_script(self, request, ammo, resp):
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

            exec(request["compiled"], context)  # noqa: S102

        except Exception:
            log.exception(
                f"Script fail\n{request['script']}\n\n{supply}\n",
            )

    @staticmethod
    def beautify_url(
        url: str,
        method: str,
        body: str | None,  # noqa: ARG004
    ) -> str:
        urlparts = urlparse(url)
        max_display_length = 15
        path = (
            urlparts.path
            if len(urlparts.path) < max_display_length
            else f"...{urlparts.path[-max_display_length:]}"
        )
        query = f"?{urlparts.query}" if urlparts.query else ""
        if urlparts.fragment:
            query += f"#{urlparts.fragment}"
        query = query if len(query) < max_display_length else f"?...{query[-max_display_length:]}"
        return f"""{method} {urlparts.netloc}{path}{query}"""

    def worker(self, thread_id: int, job: dict[str, Any]) -> None:
        """
        Thread callable.
        Strike ammo from queue.
        """
        try:
            # setup logging ASAP and as safe as possible
            if isinstance(job, dict):
                request = job.get("request", {})
                ammo_id = job.get("id", 0)
                ammo_name = request.get("name", "")
            else:
                request = {}
                ammo_id = 0
                ammo_name = ""
            request_logging.sending(thread_id, ammo_id, ammo_name)
            pretty_url = ""  # we use it in `except`
            try:
                job = apply_supply_dict(job, dict(self.supply, **job["supply"]))

                url = request.get("url", "")
                method = request.get("method", "GET")
                body = json.dumps(request["body"]) if "body" in request else None
                headers = self.get_headers(request, body is not None)
                pretty_url = self.beautify_url(url, method, body)

                log.debug(
                    f"Bomb to drop:\n{pretty_url}"  # noqa: G003
                    + ("\n{body}" if body is not None else ""),
                )
                if self.args.quiet and ammo_id in self.show_request:
                    print(f"{self.show_request[ammo_id].format(id=ammo_id):>15}\r", end="")
                log.info(pretty_url)

                start_ns = time_ns()
                status: str | int
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
                    self.status_coloured(status)  # noqa: G003
                    + f" ({pretty_sz(len(resp))}) "
                    + pretty_url
                    + " "
                    + (red(resp) if status == EXCEPTION_STATUS else ""),
                )
            except Exception as e:  # noqa: BLE001
                log.info(
                    f"{pretty_url} {red(str(e))}",
                    exc_info=True,
                )
        finally:
            request_logging.main_thread()

    def reload(
        self,
        requests: Any,
        repeat: int | None = None,
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
        log.warning(
            "\n"  # noqa: G003
            + "=" * 100
            + "\n"
            + markdown_for_terminal(self.reporter.report())
            + "=" * 100
            + "\n",
        )
