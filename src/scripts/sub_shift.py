"""
Utility script rather than interface to apply substitutions
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
    keytypes = parser.add_mutually_exclusive_group(required=True)
    keytypes.add_argument("-v", "--vigenere", type=str,
                                    help="vigenere key")
    keytypes.add_argument("-c", "--caesar", type=string_length(2),
                                    help="Caesar pairing")
    return parser.parse_args()

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
    if sys.stdin.isatty():
        sys.exit("this is a command line script")
    args = parse_args()
    if args.vigenere:
        sys.stdout.write(shift(sys.stdin.read(), args.vigenere))
    else:
        frm, to = args.caesar.upper()
        shift_char = string.ascii_uppercase[ord(frm) - ord(to)]
        sys.stdout.write(shift(sys.stdin.read(), shift_char))
