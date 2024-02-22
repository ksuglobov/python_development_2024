import cowsay
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


if __name__ == '__main__':
    main()
