from collections import Counter
import random
import argparse
from pathlib import Path
import sys
from urllib.parse import urlparse
from urllib.request import urlopen


POSSIBLE_CHOICE = ('д', 'Д', 'н', 'Н')


def positive_int(value):
    """
    Check if the value is a positive integer number.
    """
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f'invalid positive int value: {value}')


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = 0
    for c1, c2 in zip(guess, secret):
        if c1 == c2:
            bulls += 1

    cows_dict = (Counter(guess) & Counter(secret))
    cows = sum(cows_dict.values())

    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(prompt).strip()
    while not guess or valid is not None and guess not in valid:
        # surrender
        if not guess:
            ans = ''
            while ans not in POSSIBLE_CHOICE:
                ans = input('Сдаётесь? (д/н) ').lower()
            if ans.lower() == 'д':
                raise ValueError
        else:
            print(f'Такого слова нет в словаре')

        # try again
        guess = input(prompt).strip()

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))    


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    print('Слово загадано')

    solved = False
    attempts = 0
    while not solved:
        try:
            guess = ask('Введите слово: ', words)
        except ValueError:
            print(f'Загаданное слово: {secret}')
            break
        attempts += 1

        bulls, cows = bullscows(guess, secret)

        inform('Быки: {}, Коровы: {}', bulls, cows)

        if bulls == len(secret):
            solved = True
            print('Вы угадали!')

    return attempts


def is_valid_file(path):
    path = Path(path)
    return path.is_file() and path.exists()


def is_valid_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            return text
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        sys.exit(1)


def read_url(path):
    try:
        with urlopen(path) as response:
            text = response.read().decode('utf-8')
            return text
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        sys.exit(1)


def main():
    # command line arguments parser
    parser = argparse.ArgumentParser(
        description='Command-line "Bulls and cows" game.'
    )

    # dictionary
    parser.add_argument(
        'dictionary',
        type=str,
        help='Path to file or URL with dictionary of words.'
    )

    # words length
    parser.add_argument(
        'length',
        type=positive_int,
        default=5,
        nargs='?',
        help='Length of words used in the game (default: %(default)s).'
    )

    args = parser.parse_args()

    # read the words
    dict_path = args.dictionary
    if is_valid_file(dict_path):
        words = read_file(dict_path)
    elif is_valid_url(dict_path):
        words = read_url(dict_path)
    else:
        print(f'Dictionary is neither path to file nor url!')
        return

    words = words.split()

    # filter words by words length
    words = [word for word in words if len(word) == args.length]
    if not words:
        print(f'There are no words with length={args.length} in dictionary!')
        return

    # the game
    print(f'Используются слова длины {args.length}')
    attempts = gameplay(ask, inform, words)
    print(f'Число попыток: {attempts}')


if __name__ == '__main__':
    main()
