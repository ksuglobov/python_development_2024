from collections import Counter
import random

def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = 0
    for c1, c2 in zip(guess, secret):
        if c1 == c2:
            bulls += 1

    cows_dict = (Counter(guess) & Counter(secret))
    cows = sum(cows_dict.values())

    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(prompt)
    while not guess or valid is not None and guess not in valid:
        # surrender
        if not guess:
            ans = ''
            while ans != 'y' and ans != 'n':
                ans = input('Сдаётесь? (y/n)')
            if ans == 'y':
                raise ValueError

        # try again
        guess = input(prompt)

    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))    


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)

    solved = False
    attempts = 0
    while not solved:
        try:
            guess = ask("Введите слово: ", words)
        except ValueError:
            print(f'Загаданное слово: {secret}')
            break
        attempts += 1

        bulls, cows = bullscows(guess, secret)

        inform("Быки: {}, Коровы: {}", bulls, cows)

        if bulls == len(secret):
            solved = True
    
    print(attempts)