#!/usr/bin/env python3

"""
Invert the letters of text a la beaufort. Requires no parameters.
"""

import string
import sys
import argparse

from sub_shift import shift

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--offset", type=int, default=0,
                                help="extra offset")
    return parser.parse_args()

translate_dict = {ord(a): ord(b)
                        for a, b in zip(string.ascii_uppercase,
                                        reversed(string.ascii_uppercase))}
translate_dict.update({ord(a): ord(b)
                        for a, b in zip(string.ascii_lowercase,
                                        reversed(string.ascii_lowercase))})

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command line script requiring stdin")
    args = get_args()
    plain = sys.stdin.read()
    sys.stdout.write(shift(plain.translate(translate_dict),
                string.ascii_lowercase[-args.offset]))
