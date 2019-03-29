from threading import Thread
from queue import Queue
from src.terminal_colours import red, dark_red, green
from urllib.parse import urlparse
import http.client
import ssl
import json


def make_request(request: dict) -> dict:
    """
    Make HTTP request described in request.
    Returns dict with names extracted from request result if 'extract' part is specified in the request.
    And place 'status' or the response to the dict.
    """
    url = urlparse(request['url'])
    conn = http.client.HTTPSConnection(
        url.netloc,
        context=ssl._create_unverified_context()
    )
    conn.request(
        request['method'],
        url.path,
        body=json.dumps(request['body']) if 'body' in request else None,
        headers=request['headers'] if 'headers' in request else {}
    )
    resp = conn.getresponse()
    result = {'status': resp.status}
    if 'extract' in request:
        data = json.loads(resp.read())
        for name, val in request['extract'].items():
            if not val:
                val = name
            result[name] = data[val]
    return result


class Requestor:
    """
    Use horde of threads to make HTTP-requests
    """
    def __init__(self, threads, ok_statuses=[200], overload_statuses=[502, 504]):
        """
        :param threads: number of threads to use to request
        """
        self.ok = ok_statuses
        self.overload = overload_statuses
        self.queue = Queue(threads)
        for i in range(threads):
            t = Thread(target=self.do_work, args=[i])
            t.daemon = True
            t.start()

    def status_coloured(self, status: int) -> str:
        if status in self.ok:
            return green(str(status))
        elif status in self.overload:
            return dark_red(str(status))
        else:
            return red(str(status))

    def do_work(self, thread_id):
        while True:
            job = self.queue.get()
            status = make_request(job['request'])['status']
            print(f'{job["id"]} (thread {thread_id}) ', '<' * 6, self.status_coloured(status))
            self.queue.task_done()

    def add(self, job: dict):
        """
        Add job to queue
        """
        self.queue.put(job)

    def start(self):
        self.queue.join()



