import random
import string
import time

CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase


def encode(number):
    """Encodes a number using base62 encoding"""
    if number == 0:
        return CHARS[0]
    encoding = ''
    while number > 0:
        number, remainder = divmod(number, 62)
        encoding = CHARS[remainder] + encoding
    return encoding


def decode(encoded):
    """Decodes a base62 string into a number"""
    length = len(encoded)
    number = 0

    for index, char in enumerate(encoded):
        if char not in CHARS:
            raise ValueError(f'Invalid character {char} in encoded string.')
        number += CHARS.index(char) * (62 ** (length - (index + 1)))

    return number


def generate_unique_id():
    """Generates a unique ID based on timestamp and a pseudo-random number"""
    timestamp = int(time.time() * 1000)
    random_number = random.randint(0, 99)

    return int(f'{timestamp}{random_number}')
