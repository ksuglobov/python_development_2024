from collections import Counter

def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = 0
    for c1, c2 in zip(guess, secret):
        if c1 == c2:
            bulls += 1

    cows_dict = (Counter(guess) & Counter(secret))
    cows = sum(cows_dict.values())

    return bulls, cows
