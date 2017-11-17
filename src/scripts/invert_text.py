#!/usr/bin/env python3

"""
Reverse the letters of text a la beaufort
"""

import string
import sys

translate_dict = {ord(a): ord(b) for a, b in zip(string.ascii_uppercase, reversed(string.ascii_uppercase))}
translate_dict.update({ord(a): ord(b) for a, b in zip(string.ascii_lowercase, reversed(string.ascii_lowercase))})

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command line script requiring stdin")
    plain = sys.stdin.read()
    print(plain.translate(translate_dict))
