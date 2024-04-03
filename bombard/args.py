"""
Parse bombard command line args.
"""

import argparse
from typing import Any

from bombard.show_descr import markdown_for_terminal
from bombard.terminal_colours import BROWN, OFF

# from pkg_resources import resource_string


EXAMPLES_PREFIX = "bombard://"  # replaced with path to package folder
DIR_DESC_FILE_NAME = "README.md"  # if directory as campaign file then show content of this file from the directory
THREADS_NUM = 10
CAMPAIGN_FILE_NAME = "bombard.yaml"
INIT_EXAMPLE = "easy.yaml"
REPEAT = 10
THRESHOLD = 1000
TIMEOUT = 15


def get_args() -> Any:
    parser = argparse.ArgumentParser(
        description=markdown_for_terminal(
            f"""bombard: utility to bombard with HTTP-requests.

{BROWN}[GitHub](https://github.com/masterandrey/bombard){OFF}"""
        ),
        epilog=markdown_for_terminal("""To show available examples use `bombard --examples`"""),
    )
    parser.add_argument(
        dest="file_name",
        type=str,
        nargs="?",
        default=CAMPAIGN_FILE_NAME,
        help=f"""file name with bombing campaign plan (default "#{CAMPAIGN_FILE_NAME}").
To use bombard examples prefix filename with "@".""",
    )
    parser.add_argument(
        "--parallel",
        "-p",
        dest="threads",
        type=int,
        default=THREADS_NUM,
        help=f"number of simultaneous requests (default {THREADS_NUM})",
    )
    parser.add_argument(
        "--supply",
        "-s",
        dest="supply",
        type=str,
        nargs="*",
        help='supply as separate pairs "-s name=val" or many pairs at once "-s name1=val1,name2=val2,.."',
    )
    parser.add_argument(
        "--repeat",
        "-r",
        dest="repeat",
        type=int,
        default=REPEAT,
        help=f"how many times to repeat (by default {REPEAT})",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        default=False,
        action="store_true",
        help="verbose output (by default False)",
    )
    parser.add_argument(
        "--version",
        dest="version",
        default=False,
        action="store_true",
        help="bombard version",
    )
    parser.add_argument("--log", "-l", dest="log", type=str, default=None, help="log file name")
    parser.add_argument(
        "--ms",
        "-m",
        dest="ms",
        default=False,
        action="store_true",
        help="Show all times in ms (by default use intellectual format)",
    )
    parser.add_argument(
        "--threshold",
        "-t",
        dest="threshold",
        type=int,
        default=THRESHOLD,
        help=f"threshold in ms. all times greater than that will be shown in red (default {THRESHOLD})",
    )
    parser.add_argument(
        "--timeout",
        dest="timeout",
        type=int,
        default=TIMEOUT,
        help=f"http timeout in seconds (default {TIMEOUT})",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        dest="quiet",
        default=False,
        action="store_true",
        help="suppress printing request/response to improve performance",
    )
    parser.add_argument(
        "--example",
        "-e",
        dest="example",
        type=str,
        default=None,
        help="""get bombard campaign from internal bombard example with the name.
to list all available examples use `--examples`.""",
    )
    parser.add_argument(
        "--examples",
        "-x",
        dest="examples",
        default=False,
        action="store_true",
        help="""show all available examples description.""",
    )
    parser.add_argument(
        "--dry",
        "-d",
        dest="dry",
        default=False,
        action="store_true",
        help='run without actual HTTP requests. if there is "dry" parameter in an ammo use it as fake request result.',
    )
    parser.add_argument(
        "--init",
        "-i",
        dest="init",
        default=False,
        action="store_true",
        help=f"""copy `{INIT_EXAMPLE}` example to current folder with the name {CAMPAIGN_FILE_NAME}
so it will be used as default with `bombard` command. If you want to copy different example add option
`--example <the name you want>`. For full list of examples use `--examples` option.
""",
    )

    args = parser.parse_args()
    args.parser = parser

    return args
