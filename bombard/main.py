"""
Bombard's main
"""
from bombard.campaign_yaml import yaml
from bombard.bombardier import Bombardier
import logging
from bombard.args import get_args
from typing import Optional


log = logging.getLogger()


def guess_type(value: str):
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


def setup_logging(level: int, log_file_name: Optional[str]):
    log.setLevel(level)
    if log_file_name is not None:
        log.addHandler(
            logging.FileHandler(log_file_name)
        )


def get_supply_from_cli(supply: Optional[list]):
    result = {}
    if supply:
        for item in supply:
            for var in item.split(','):
                name, val = var.split('=')
                result.update({name: guess_type(val)})
    return result


def load_book_supply(cli_supply, book_supply):
    """
    Updates CLI supply with supply from campaign book.
    But do not overwrite CLI supply with book supply - values from CLI have bigger priority.
    """
    for var, val in book_supply.items():
        if var not in cli_supply:
            cli_supply[var] = val.format(**cli_supply) if isinstance(val, str) else val


def add_names_to_requests(campaign_book):
    """
    Duplicate names inside requests so worker will see it and use in stat report
    """
    for request_set in ['prepare', 'ammo']:
        if request_set in campaign_book:
            for name, request in campaign_book[request_set].items():
                request['name'] = name


def campaign(args):
    if args.quiet:
        level = logging.ERROR
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    setup_logging(level=level, log_file_name=args.log)

    log.debug(f'Starting bombard campaign with args\n' + ' '*4 + f'{args.__dict__}')

    supply = get_supply_from_cli(args.supply)

    campaign_book = yaml.load(open(args.file_name, 'r'))
    log.debug(f'Loaded bombard campaign from "{args.file_name}": {len(campaign_book["ammo"])} ammo.')

    load_book_supply(supply, campaign_book.get('supply', {}))
    log.debug(f'Supply: {supply}')

    add_names_to_requests(campaign_book)

    bombardier = Bombardier(supply, args, campaign_book)
    if 'prepare' in campaign_book:
        requests = campaign_book['prepare']
        repeat = 1
    else:
        requests = campaign_book['ammo']
        repeat = args.repeat
    for ammo in requests.values():
        bombardier.reload(ammo, repeat=repeat)
    bombardier.bombard()


def main():
    campaign(get_args())


if __name__ == '__main__':
        main()
