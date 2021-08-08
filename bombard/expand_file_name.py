import os.path

import bombard
from bombard.args import CAMPAIGN_FILE_NAME, DIR_DESC_FILE_NAME, EXAMPLES_PREFIX
from bombard.show_descr import markdown_for_terminal
from bombard.terminal_colours import red


def expand_relative_file_name(file_name):
    """
    Replace RELATIVE_PREFIX with package folder so bombard script can use internal examples without full path spec
    """
    if file_name.strip().startswith(EXAMPLES_PREFIX):
        # resource_string(__name__, args.file_name[1:])  # recommended use resource to be zipfile compatible. but this is a pain for !include
        return os.path.join(
            os.path.dirname(bombard.__file__), "examples", file_name[len(EXAMPLES_PREFIX) :]
        )
    else:
        return file_name


def get_campaign_file_name(args):
    if args.example is not None:
        if args.file_name != CAMPAIGN_FILE_NAME:
            print(red(f'--example option found - ignoring campaign file name "{args.file_name}".'))
        args.file_name = EXAMPLES_PREFIX + args.example
        if not args.file_name.endswith(".yaml"):
            args.file_name += ".yaml"
    if args.examples:
        if args.file_name != CAMPAIGN_FILE_NAME:
            print(
                red(f'--examples option found - ignoring campaign file name "{args.file_name}".')
            )
        if args.example is not None:
            print(red("Please do not use --example and --examples options simultaneously."))
        args.file_name = EXAMPLES_PREFIX

    return expand_relative_file_name(args.file_name)


def show_folder(folder_path):
    file_name = os.path.join(folder_path, DIR_DESC_FILE_NAME)
    if not os.path.isfile(file_name):
        print(f"\nNo {DIR_DESC_FILE_NAME} in folder {folder_path}. \nFolder content:\n")
        for name in os.listdir(folder_path):
            print(name)
    else:
        print(f"\n{folder_path}:\n")
        with open(file_name, "r") as desc:
            print(markdown_for_terminal(desc.read()))
