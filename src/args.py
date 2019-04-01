import sys
import os.path
from src.terminal_colours import red
import argparse


THREADS_NUM = 100
CAMPAIGN_FILE_NAME = 'bombard.yaml'
REPEAT = 100
THRESHOLD = 1000


def get_args():
    parser = argparse.ArgumentParser(
        description='bombard: utility to bombard with HTTP-requests.',
        epilog='See examples of requests files (yaml or py) on https://github.com/masterandrey/bombard'
    )
    parser.add_argument(
        dest='file_name', type=str, nargs='?',
        default=CAMPAIGN_FILE_NAME,
        help=f'file name with bombing campaign plan (default "{CAMPAIGN_FILE_NAME}")'
    )
    parser.add_argument(
        '--parallel', '-p', dest='threads', type=int,
        default=THREADS_NUM,
        help=f'number of simultaneous requests (default {THREADS_NUM})'
    )
    parser.add_argument(
        '--supply', '-s', dest='supply', type=str, nargs='*',
        help='supply as separate pairs "-c name=val" or many pairs at once "-c name1=val1,name2=val2,.."'
    )
    parser.add_argument(
        '--repeat', '-r', dest='repeat', type=int, default=REPEAT,
        help=f'how many times to repeat (by default {REPEAT})'
    )
    parser.add_argument(
        '--verbose', '-v', dest='verbose', default=False, action='store_true',
        help=f'verbose output (by default False)'
    )
    parser.add_argument(
        '--log', '-l', dest='log', type=str, default=None,
        help=f'log file name'
    )
    parser.add_argument(
        '--ms', '-m', dest='log', default=False, action='store_true',
        help=f'Show all times in ms (by default use intellectual format)'
    )
    parser.add_argument(
        '--threshold', '-t', dest='threshold', type=int, default=THRESHOLD,
        help=f'threshold in ms. all times greater than that will be shown in red (default {THRESHOLD})'
    )

    args = parser.parse_args()
    if not os.path.isfile(args.file_name):
        print(red(f'\nCannot find campaign file "{args.file_name}"\n'))
        parser.print_help(sys.stderr)
        exit(1)

    return args


