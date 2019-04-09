"""
Use local thread storage to add to log information about request
"""
import threading
import logging
from bombard.terminal_colours import OFF, GRAY


thread_data = threading.local()


def sending(thread_id, request_id, request_name):
    """
    Start sending request
    """
    global thread_data
    thread_data.thread_id = thread_id
    thread_data.request_id = request_id
    thread_data.request_name = request_name
    thread_data.dir = '>' * 3
    thread_data.colour = GRAY


def receiving():
    """
    Got response to request
    """
    global thread_data
    thread_data.dir = '<' * 3
    thread_data.colour = OFF


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.threadid = thread_data.thread_id
        record.requestid = str(thread_data.request_id).rjust(4)
        record.colour = thread_data.colour
        record.requestname = thread_data.request_name
        record.dir = thread_data.dir
        return super().format(record)


handler = logging.StreamHandler()
handler.setFormatter(
    RequestFormatter(
        fmt=f'%(colour)s%(asctime)s %(requestid)s (thread %(threadid)s) %(requestname)s %(dir)s %(message)s{OFF}',
        datefmt='%-d %b %H:%M:%S'
    )
)
logging.getLogger().handlers = []
logging.getLogger().addHandler(handler)