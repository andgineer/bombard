"""
Bombard's main code
"""
import argparse
from src.yaml_includes import yaml
from src.bombardier import Bombardier
import logging
import sys
import os.path
from src.terminal_colours import red


log = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(message)s')


THREADS_NUM = 100
CAMPAIGN_FILE_NAME = 'bombard.yaml'
REPEAT = 100


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
        '--threads', dest='threads', type=int,
        default=THREADS_NUM,
        help=f'number of threads (default {THREADS_NUM})'
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
    args = parser.parse_args()
    if not os.path.isfile(args.file_name):
        print(red(f'\nCannot find campaign file "{args.file_name}"\n'))
        parser.print_help(sys.stderr)
        exit(1)
    return args


def campaign(args):
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    # get supply vars from command line
    supply = {}
    if args.supply:
        for vars in args.supply:
            for var in vars.split(','):
                supply.update(dict([var.split('=')]))
    log.debug(f'Starting bombard campaign with args\n' + ' '*4 + f'{args.__dict__}')
    campaign_book = yaml.load(open(args.file_name, 'r'))
    log.debug(f'Loaded bombard campaign from "{args.file_name}": {len(campaign_book["ammo"])} ammo.')

    # add supply from campaign file
    for var, val in campaign_book['supply'].items():
        if var not in supply:  # dbombardiero not redefine if already defined from command line
            supply[var] = val.format(**supply)
    log.debug(f'Supply: {supply}')

    bombardier = Bombardier(supply, args, campaign_book)
    if 'prepare' in campaign_book:
        requests = campaign_book['prepare']
    else:
        requests = campaign_book['ammo']
    for ammo in requests.values():
        bombardier.reload(ammo)
    bombardier.bombard()


def main():
    campaign(get_args())


if __name__ == '__main__':
        main()
