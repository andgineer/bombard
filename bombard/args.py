"""
Parse bombard command line args
"""
import sys
import os.path
from bombard.terminal_colours import red, BROWN, OFF
import argparse
import bombard
from bombard.show_descr import markdown_for_terminal
# from pkg_resources import resource_string


EXAMPLES_PREFIX = 'bombard://'  # replaced with path to package folder
DIR_DESC_FILE_NAME = 'README.md'  # if directory as campaign file then show content of this file from the directory
THREADS_NUM = 10
CAMPAIGN_FILE_NAME = 'bombard.yaml'
REPEAT = 10
THRESHOLD = 1000
TIMEOUT = 10


def expand_relative_file_name(file_name):
    """
    Replace RELATIVE_PREFIX with package folder so bombard script can use internal examples without full path spec
    """
    if file_name.strip().startswith(EXAMPLES_PREFIX):
        # resource_string(__name__, args.file_name[1:])  # recommended use resource to be zipfile compatible. but this is a pain for !include
        return os.path.join(os.path.dirname(bombard.__file__), 'examples', file_name[len(EXAMPLES_PREFIX):])
    else:
        return file_name


def get_args():
    parser = argparse.ArgumentParser(
        description=markdown_for_terminal(f'''bombard: utility to bombard with HTTP-requests.

{BROWN}[GitHub](https://github.com/masterandrey/bombard){OFF}'''),
        epilog=markdown_for_terminal('''To show available examples use `bombard --examples`''')
    )
    parser.add_argument(
        dest='file_name', type=str, nargs='?',
        default=CAMPAIGN_FILE_NAME,
        help=f'''file name with bombing campaign plan (default "#{CAMPAIGN_FILE_NAME}").
To use bombard examples prefix filename with "@".'''
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
        '--ms', '-m', dest='ms', default=False, action='store_true',
        help=f'Show all times in ms (by default use intellectual format)'
    )
    parser.add_argument(
        '--threshold', '-t', dest='threshold', type=int, default=THRESHOLD,
        help=f'threshold in ms. all times greater than that will be shown in red (default {THRESHOLD})'
    )
    parser.add_argument(
        '--timeout', dest='timeout', type=int, default=TIMEOUT,
        help=f'http timeout in seconds (default {TIMEOUT})'
    )
    parser.add_argument(
        '--quiet', '-q', dest='quiet', default=False, action='store_true',
        help=f'suppress printing request/response to improve performance'
    )
    parser.add_argument(
        '--example', '-e', dest='example', type=str, default=None,
        help=f'''get bombard campaign from internal bombard example with the name. 
to list all available examples use `--examples`.'''
    )
    parser.add_argument(
        '--examples', '-x', dest='examples', default=False, action='store_true',
        help=f'''show all available examples description.'''
    )

    args = parser.parse_args()

    if args.example is not None:
        if args.file_name != CAMPAIGN_FILE_NAME:
            print(red(f'--example option found - ignoring campaign file name "{args.file_name}".'))
        args.file_name = EXAMPLES_PREFIX + args.example
        if not args.file_name.endswith('.yaml'):
            args.file_name += '.yaml'
    if args.examples:
        if args.file_name != CAMPAIGN_FILE_NAME:
            print(red(f'--examples option found - ignoring campaign file name "{args.file_name}".'))
        if args.example is not None:
            print(red('Please do not use --example and --examples options simultaneously.'))
        args.file_name = EXAMPLES_PREFIX

    args.file_name = expand_relative_file_name(args.file_name)

    if os.path.isdir(args.file_name):
        file_name = os.path.join(args.file_name, DIR_DESC_FILE_NAME)
        if not os.path.isfile(file_name):
            print(f'\nNo {DIR_DESC_FILE_NAME} in folder {args.file_name}. \nFolder content:\n')
            for name in os.listdir(args.file_name):
                print(name)
        else:
            print(f'\n{args.file_name}:\n')
            print(markdown_for_terminal(open(file_name, 'r').read()))
    print(args.file_name)

    if not os.path.isfile(args.file_name):
        print(red(f'\nCannot find campaign file "{args.file_name}"\n'))
        parser.print_help(sys.stderr)
        exit(1)

    return args


