from cowsay import Option as default_cow, cowsay, list_cows
import argparse


def list_cows_mode():
    cows = list_cows()
    print(cows)


def cowsay_mode(args):
    cowsay(...)


def main():
    # command line arguments parser
    parser = argparse.ArgumentParser(
        description='Command-line interface for python package python-cowsay'
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
        default=False,
        help='Disable message wrapping by message width (default: False).',
        dest='not_wrapping'
    )
    parser.add_argument(
        '-W',
        type=int,
        default=40,
        help='Width to wrap the message (default: %(default)s). Works if wrapping is enabled.',
        dest='width'
    )

    # cow itself
    parser.add_argument(
        '-f',
        type=str,
        default="default",
        help='Either the name of a cow from cowpath (default: %(default)s) or path to cowfile.',
        dest='cow'
    )

    # cow mode
    cow_mode_parser = parser.add_argument_group(
        title='Cow mode',
        description='Affects the appearance of the cow. If multiple modes are given, the one furthest down in this list is selected'
    )
    cow_modes = ['Borg', 'dead', 'greedy', 'paranoid', 'stoned', 'tired', 'wired', 'young']
    for cow_mode in cow_modes:
        key = cow_mode[0].lower()
        cow_mode_parser.add_argument(f'-{key}', action='store_const', const=key, help=cow_mode)

    # cow parameters
    parser.add_argument(
        '-e',
        type=str,
        default=default_cow.eyes,
        help='Cow\'s eyes string (default: %(default)s). Works if no cow mode specified.',
        dest='eyes'
    )
    parser.add_argument(
        '-T',
        type=str,
        default=default_cow.tongue,
        help='Cow\'s tongue string (default: %(default)s). Works if no cow mode specified.',
        dest='tongue'
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
