"""
Bombard's main code
"""
import argparse
import sys
import argparse
from src import yaml_loader
from src.requestor import Requestor, make_request


THREADS_NUM = 100
REQUESTS_FILE_NAME = 'bombard.yaml'
REPEAT = 100


def apply_context(request: dict, context: dict) -> dict:
    """
    Use context to substitute all {name} in request strings.
    """
    for name in request:
        if isinstance(request[name], dict):
            request[name] = apply_context(request[name], context)
        if isinstance(request[name], str):
            request[name] = request[name].format(**context)
    return request


def set_up(play_book: dict):
    """
    Execute HTTP requests from play book (presumably loaded from setUp section of yaml definitions).
    Returns dict with names extracted from the requests results
    """
    result = {}
    for request in play_book.values():
        result.update(make_request(request))
    return result


def get_args():
    parser = argparse.ArgumentParser(
        description='bombard: utility to bombard with HTTP-requests.'
    )
    parser.add_argument(
        dest='file_name', type=str, nargs='?',
        default=REQUESTS_FILE_NAME,
        help=f'requests file name (default "{REQUESTS_FILE_NAME}")'
    )
    parser.add_argument(
        '--threads', dest='threads', type=int,
        default=THREADS_NUM,
        help=f'number of threads (default {THREADS_NUM})'
    )
    parser.add_argument(
        '--var', '-v', dest='vars', type=str, nargs='*',
        help='vars as "name=val"'
    )
    parser.add_argument(
        '--repeat', '-r', dest='repeat', type=int, default=REPEAT,
        help=f'how many times to repeat (by defaul {REPEAT})'
    )
    return parser.parse_args()


def main():
    args = get_args()
    play_book = yaml_loader.load(args.file_name)
    if args.vars:
        context = dict([var.split('=') for var in args.vars])
    else:
        context = {}
    for var, val in play_book['vars'].items():
        if var not in context:
            context[var] = val.format(**context)
    print(f'Use vars: {context}')
    set_up_requests = apply_context(play_book['setUp'], context)
    context.update(set_up(set_up_requests))
    bombard_requests = apply_context(play_book['bombard'], context)

    requestor = Requestor(args.threads)
    try:
        request_id = 0
        for counter in range(args.repeat):
            for request in bombard_requests.values():
                for _ in range(request.get('repeat', 1)):
                    requestor.add({'id': request_id, 'request': request})
                    request_id += 1
        requestor.start()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
        main()
