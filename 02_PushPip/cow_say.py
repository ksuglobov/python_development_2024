from cowsay import cowsay, Option as default_cow,
import argparse


def main():
    # command line arguments parser
    parser = argparse.ArgumentParser(
        description='Command-line interface for python package python-cowsay'
    )

    # message parameters
    parser.add_argument(
        'message',
        type=str,
        help='The message you want the cow to say.'
    )
    parser.add_argument('-n',
        action='store_true',
        default=False,
        help='Disable message wrapping by message width (default: False).',
        dest='not_wrapping'
    )
    parser.add_argument('-W',
        type=int,
        default=40,
        help='Width to wrap the message (default: %(default)s). Works if wrapping is enabled.',
        dest='width'
    )

    # cow parameters
    parser.add_argument('-f',
        type=str,
        default="default",
        help='Either the name of a cow specified in the COWPATH (default: %(default)s) or path to cowfile.',
        dest='cow'
    )

    cow_mode_parser = parser.add_argument_group(
        title='Cow mode',
        description='Affects the appearance of the cow. If multiple modes are given, the one furthest down in this list is selected'
    )
    cow_mode_parser.add_argument('-b', action='store_const', const='b', help='Borg')
    cow_mode_parser.add_argument('-d', action='store_const', const='d', help='dead')
    cow_mode_parser.add_argument('-g', action='store_const', const='g', help='greedy')
    cow_mode_parser.add_argument('-p', action='store_const', const='p', help='paranoid')
    cow_mode_parser.add_argument('-s', action='store_const', const='s', help='stoned')
    cow_mode_parser.add_argument('-t', action='store_const', const='t', help='tired')
    cow_mode_parser.add_argument('-w', action='store_const', const='w', help='wired')
    cow_mode_parser.add_argument('-y', action='store_const', const='y', help='young')

    parser.add_argument('-e',
        type=str,
        default=default_cow.eyes,
        help='Cow\'s eyes string (default: %(default)s). Works if no cow mode specified.',
        dest='eyes'
    )
    parser.add_argument('-T',
        type=str,
        default=default_cow.tongue,
        help='Cow\'s tongue string (default: %(default)s). Works if no cow mode specified.',
        dest='tongue'
    )


if __name__ == '__main__':
    main()
