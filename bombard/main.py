"""
Bombard's main
"""
import logging
import os.path
from shutil import copyfile
from typing import Any, Dict, List, Optional, Union

import colorama

import bombard
from bombard.args import CAMPAIGN_FILE_NAME, EXAMPLES_PREFIX, INIT_EXAMPLE, get_args
from bombard.bombardier import AMMO, PREPARE, Bombardier
from bombard.campaign_yaml import yaml
from bombard.expand_file_name import expand_relative_file_name, get_campaign_file_name, show_folder
from bombard.request_logging import log, setup_logging
from bombard.terminal_colours import OFF, RED, red

colorama.init()  # On Windows will filter ANSI escape sequences out of any text sent to
# stdout or stderr, and replace them with equivalent Win32 calls.


def guess_type(value: str) -> Union[str, int, float]:
    """
    Converts value in int or float if possible
    """
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def get_supply_from_cli(supply: Optional[List[str]]) -> Dict[str, Any]:
    """
    Extract key=value pairs from list of `supply` args
    """
    result = {}
    if supply:
        for item in supply:
            for var in item.split(","):
                name, val = var.split("=")
                result.update({name: guess_type(val)})
    return result


def load_book_supply(cli_supply: Dict[str, Any], book_supply: Dict[str, Any]) -> None:
    """
    Updates CLI supply with supply from campaign book.
    But do not overwrite CLI supply with book supply - values from CLI have bigger priority.
    """
    for var, val in book_supply.items():
        if var not in cli_supply:
            cli_supply[var] = val.format(**cli_supply) if isinstance(val, str) else val


def add_names_to_requests(campaign_book: Dict[str, Any]) -> None:
    """
    Duplicate names inside requests so worker will see it and use in stat report
    """
    for request_set in [PREPARE, AMMO]:
        if request_set in campaign_book:
            for name, request in campaign_book[request_set].items():
                request["name"] = name


def init(args: Any) -> None:
    """
    Copies the example to current folder as bombard.yaml
    """
    if args.example is None:
        src = expand_relative_file_name(f"{EXAMPLES_PREFIX}{INIT_EXAMPLE}")
    else:
        src = get_campaign_file_name(args)  # actually it will be from ==example
    if os.path.isfile(CAMPAIGN_FILE_NAME):
        print(f"Cannot init from {src}:\n{RED}File {CAMPAIGN_FILE_NAME} already exists.{OFF}")
        return
    copyfile(src, CAMPAIGN_FILE_NAME)
    # todo copy external python scripts if it is included into the example (create yaml CopyLoader)


def start_campaign(args: Any, campaign_book: Dict[str, Any]) -> None:
    log.debug(  # pylint: disable=logging-not-lazy
        "Starting bombard campaign with args\n" + " " * 4 + f"{args.__dict__}"
    )
    log.debug(
        f'Loaded bombard campaign from "{args.file_name}": {len(campaign_book.get("ammo", {}))} ammo.'
    )
    if PREPARE not in campaign_book and AMMO not in campaign_book:
        print(
            f'You should have at least one of "{PREPARE}" and "{AMMO}" '
            f"section in your campaign file {args.file_name}"
        )
        return

    supply = get_supply_from_cli(args.supply)
    load_book_supply(supply, campaign_book.get("supply", {}))
    log.debug(f"Supply: {supply}")

    add_names_to_requests(campaign_book)

    bombardier = Bombardier(args, campaign_book, supply)
    if PREPARE in campaign_book:
        for ammo in campaign_book[PREPARE].values():
            bombardier.reload(ammo, repeat=1, prepare=True)
        bombardier.process()
    if not bombardier.request_fired and AMMO in campaign_book:
        for ammo in campaign_book[AMMO].values():
            bombardier.reload(ammo, repeat=args.repeat)
        bombardier.process()
    bombardier.stop()
    bombardier.report()


def campaign(args: Any) -> None:
    if args.version:
        print(bombard.__name__, bombard.version())
        with open(
            os.path.join(os.path.dirname(bombard.__file__), "LICENSE.txt"), "r", encoding="utf8"
        ) as license:
            print(license.readline())
        return

    if args.quiet:
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    setup_logging(level=level, log_file_name=args.log)

    if args.init:
        init(args)
        return

    campaign_file_name = get_campaign_file_name(args)
    if os.path.isdir(campaign_file_name):
        show_folder(campaign_file_name)
    elif not (os.path.isfile(campaign_file_name) or args.init):
        print(red(f'\nCannot find campaign file "{args.file_name}"\n'))
    else:
        start_campaign(args, yaml.load(open(campaign_file_name, "r", encoding="utf8")))


def main() -> None:
    campaign(get_args())


if __name__ == "__main__":
    main()
