from threading import Thread
from queue import Queue
from bombard.terminal_colours import red, dark_red, green, gray
from bombard.attr_dict import AttrDict
from urllib.parse import urlparse
import http.client
import ssl
import json
from copy import deepcopy
import logging


log = logging.getLogger()

DEFAULT_OK = [200]
DEFAULT_OVERLOAD = [502, 504]


def apply_supply(request: dict, supply: dict) -> dict:
    """
    Use supply to substitute all {name} in request strings.
    """
    for name in request:
        if isinstance(request[name], dict):
            request[name] = apply_supply(request[name], supply)
        if isinstance(request[name], str):
            request[name] = request[name].format(**supply)
    return request


class Bombardier:
    """
    Use horde of threads to make HTTP-requests
    """
    def __init__(self, supply: dict=None, args=None, campaign_book: dict=None, ok_statuses=None,
                 overload_statuses=None):
        """
        :param args.threads: number of threads to use to request
        """
        self.supply = supply
        self.args = args
        self.campaign = campaign_book
        self.ok = ok_statuses if ok_statuses is not None else DEFAULT_OK
        self.overload = overload_statuses if overload_statuses is not None else DEFAULT_OVERLOAD
        self.queue = Queue(args.threads)
        self.job_count = 0
        for i in range(args.threads):
            t = Thread(target=self.strike, args=[i])
            t.daemon = True
            t.start()

    def status_coloured(self, status: int) -> str:
        if status in self.ok:
            return green(str(status))
        elif status in self.overload:
            return dark_red(str(status))
        else:
            return red(str(status))

    @staticmethod
    def get_headers(request: dict) -> dict:
        """
        Treat special value 'json' as Content-Type: application/json
        """
        predefined = {
            'json': {'Content-Type': 'application/json'},
        }
        if 'headers' not in request:
            return {}
        if isinstance(request['headers'], str):
            for known in predefined:
                if request['headers'].lower() == known:
                    return predefined[known]
        result = {}
        for name, val in request['headers'].items():
            for known in predefined:
                if name.lower() == known:
                    result.update(predefined[known])
                    break
            else:
                result.update({name: val})
        return result

    def process_resp(self, ammo: dict, status: int, resp: str):
        request = ammo['request']
        if status in self.ok:
            log.debug(f'{status} reply\n{resp}')
            if 'extract' in request:
                try:
                    data = json.loads(resp)
                    for name, val in request['extract'].items():
                        if not val:
                            val = name
                        self.supply[name] = data[val]
                except Exception as e:
                    log.error(f'Cannot extract {request["extract"]} from {resp}:\n{e}', exc_info=True)
            if 'script' in request:
                try:
                    # Supply immediately repeats all changes in the self.supply so if the script spawns new
                    # requests they already get new values
                    supply = AttrDict(self.supply, **ammo['supply'])
                    context = {
                        'reload': self.reload,
                        'resp': json.loads(resp),
                        'args': self.args,
                        'supply': supply,
                        'ammo': AttrDict(self.campaign['ammo'])
                    }
                    exec(request["script"], context)
                    exit()
                except Exception as e:
                    log.error(f'Script fail\n{e}\n\n{request["script"]}\n\n{supply}\n', exc_info=True)
        else:
            log.error(f'{status} reply\n{resp}')

    @staticmethod
    def beautify_url(url, method, body):
        urlparts = urlparse(url)
        path = urlparts.path if len(urlparts.path) < 15 else '...' + urlparts.path[:-15]
        query = '?' + urlparts.query if urlparts.query else ''
        if urlparts.fragment:
            query += '#' + urlparts.fragment
        query = query if len(query) < 15 else '?...' + query[:-15]
        return f"""{method} {urlparts.netloc}{path}{query}"""

    def strike(self, thread_id):
        """
        Thread callable.
        Strike ammo from queue.
        """
        while True:
            ammo = deepcopy(self.queue.get())
            ammo = apply_supply(ammo, dict(self.supply, **ammo['supply']))
            request = ammo['request']

            url = request['url']
            method = request['method'] if 'method' in request else 'GET'
            body = json.dumps(request['body']) if 'body' in request else None
            headers = self.get_headers(request)
            pretty_url = self.beautify_url(url, method, body)

            log.debug(f'Bomb to drop:\n{pretty_url}\n{body}')
            print(gray(f'{ammo["id"]:>4} (thread {thread_id:>3}) ' + '>' * 6 + ' ' + pretty_url))

            status, resp = self.make_request(url, method, headers, body)
            self.process_resp(ammo, status, resp)

            print(f'{ammo["id"]:>4} (thread {thread_id:>3}) ', '<' * 6,
                  self.status_coloured(status), pretty_url)
            self.queue.task_done()

    def make_request(self, url: str, method: str, headers: dict, body: str=None) -> (int, dict):
        """
        Make HTTP request described in request.
        Returns dict with names extracted from request result if 'extract' part is specified in the request.
        And place 'status' or the response to the dict.
        """
        url = urlparse(url)
        conn = http.client.HTTPSConnection(
            url.netloc,
            context=ssl._create_unverified_context(),
            timeout=self.args.timeout,
        )
        conn.request(method, url.path, body=body, headers=headers)
        resp = conn.getresponse()
        return resp.status, resp.read()

    def reload(self, requests, repeat=None, **kwargs):
        """
        Add request(s) to the bombardier queue `repeat`-times (args.repeat if None).
        If `repeat` field exists in the request additionally repeats as defined by it.

        Requests can be one request or list of requests.
        If supply specified it'll be used in addition to self.supply
        """
        if not isinstance(requests, list):
            requests = [requests]
        if repeat is None:
            repeat = self.args.repeat
        for request in requests:
            for _ in range(repeat):
                for __ in range(request.get('repeat', 1)):
                    self.job_count += 1
                    self.queue.put({
                        'id': self.job_count,
                        'request': request,
                        'supply': kwargs
                    })

    def bombard(self):
        self.queue.join()



