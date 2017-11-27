#!/usr/bin/env python3

"""
Script to try substitution ciphers given a keyword (useful only if you actually
know the keyword. Currently supports caesar (-c) and vigenere (-v)
"""

import sys
import string
import itertools
import argparse

def string_length(n):
    def parse_str(stri):
        if len(stri) != n:
            raise ValueError("This string should have length {}".format(n))
        return stri
    return parse_str

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    keytypes = parser.add_mutually_exclusive_group(required=True)
    keytypes.add_argument("-v", "--vigenere", type=str,
                                    help="vigenere key")
    keytypes.add_argument("-c", "--caesar", type=string_length(2), nargs="+",
                                    help="Caesar pairing")
    return parser.parse_args()

alpha_set = set(string.ascii_letters)

def shiftch(char, shift):
    return match_case(
                chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A')),
                char)

def match_case(new, old):
    return new.upper() if old.isupper() else new.lower()

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
    args = parse_args()
    if args.vigenere:
        sys.stdout.write(shift(args.input.read(), args.vigenere))
    else:
        shift_chars = "".join(string.ascii_uppercase[ord(pair[0]) - ord(pair[1])] for pair in map(str.upper, args.caesar))
        print("key was {}".format(shift_chars))
        sys.stdout.write(shift(args.input.read(), shift_chars))
