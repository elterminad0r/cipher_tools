"""
Small vigenere utility script given passphrase
"""

import sys
import string
import itertools

alpha_set = set(string.ascii_letters)

def shiftch(char, shift):
    return chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))

def shift(plain, passphrase):
    out = []
    shifts = itertools.cycle(passphrase)
    for ch in plain:
        if ch in alpha_set:
            out.append(shiftch(ch, ord('A') - ord(next(shifts).upper())))
        else:
            out.append(ch)
    return "".join(out)

if __name__ == "__main__":
    sys.stdout.write(shift(iter(lambda: sys.stdin.read(1), ""), sys.argv[1]))
