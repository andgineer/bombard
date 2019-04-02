"""
Bombard's main code
"""
from bombard.yaml_includes import yaml
from bombard.bombardier import Bombardier
import logging
from bombard.args import get_args


log = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(message)s')


def campaign(args):
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if args.log is not None:
        log.addHandler(
            logging.FileHandler(args.log)
        )

    # consoleHandler = logging.StreamHandler()
    # log.addHandler(consoleHandler)

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
