"""
Encipher plaintext using autokey
"""

import argparse
import string
import itertools

from collections import deque

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("key", type=str, help="key for encryption")
    return parser.parse_args()

def charshift(ch, kch):
    if ch.isupper():
        return string.ascii_uppercase[(ord(ch) + ord(kch.upper()) - 130) % 26]
    return string.ascii_uppercase[(ord(ch) + ord(kch.lower()) - 97 * 2) % 26]

def auto_encipher(plaintext, key):
    key = itertools.chain(key, filter(str.isalpha, plaintext))
    out = []
    for ch in plaintext:
        if ch.isalpha():
            out.append(charshift(ch, next(key)))
        else:
            out.append(ch)
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    print(auto_encipher(args.input.read(), args.key))
