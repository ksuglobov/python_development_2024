import sys
from cowsay import Option as default_cow, cowsay, list_cows
import argparse


COW_MODES = [
    'Borg',
    'dead',
    'greedy',
    'paranoid',
    'stoned',
    'tired',
    'wired',
    'young'
]

def get_cow_mode(args):
    args = vars(args)
    for cow_mode in COW_MODES[::-1]:
        key = cow_mode[0].lower()
        value = args[key]
        if value:
            return value
    return None


def list_cows_mode():
    cows = list_cows()

    print(cows)


def cowsay_mode(args):
    message = args.message
    if message is None:
        message = sys.stdin.read()

    res = cowsay(        
        message=message,
        cow=args.cow,
        preset=get_cow_mode(args),
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=not args.not_wrapping,
    )

    print(res)


def main():
    # command line arguments parser
    parser = argparse.ArgumentParser(
        description='Command-line interface for python package python-cowsay.'
    )

    # message parameters
    parser.add_argument(
        'message',
        type=str,
        nargs='?',
        help='The message you want the cow to say. If not given, stdin is used instead.'
    )
    parser.add_argument(
        '-n',
        action='store_true',
        dest='not_wrapping',
        help='Disable message wrapping by message width (default: False).'
    )
    parser.add_argument(
        '-W',
        type=int,
        default=40,
        dest='width',
        help='Width to wrap the message (default: %(default)s). Works if wrapping is enabled.'
    )

    # cow itself
    parser.add_argument(
        '-f',
        type=str,
        default='default',
        dest='cow',
        help='Name of a cow from cowpath (default: %(default)s).'
    )

    # cow mode
    cow_mode_parser = parser.add_argument_group(
        title='Cow mode',
        description='Mode affects the appearance of the cow. If multiple modes are given, the one furthest down in this list is selected.'
    )
    for cow_mode in COW_MODES:
        key = cow_mode[0].lower()
        cow_mode_parser.add_argument(f'-{key}', action='store_const', const=key, help=cow_mode)

    # cow parameters
    parser.add_argument(
        '-e',
        type=str,
        default=default_cow.eyes,
        dest='eyes',
        help='Cow\'s eyes string (default: %(default)s). Works if no cow mode specified.'
    )
    parser.add_argument(
        '-T',
        type=str,
        default=default_cow.tongue,
        dest='tongue',
        help='Cow\'s tongue string (default: %(default)s). Works if no cow mode specified.'
    )

    # list cows
    parser.add_argument(
        '-l',
        action='store_true',
        help='List all cows in the cowpath and exit.'
    )

    args = parser.parse_args()

    if args.l:
        list_cows_mode()
    else:
        cowsay_mode(args)


if __name__ == '__main__':
    main()
