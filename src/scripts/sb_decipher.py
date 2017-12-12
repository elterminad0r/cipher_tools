"""
Decipher a substitution cipher
"""

import argparse
import string

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("key", type=str, help="the key")
    return parser.parse_args()

def form_key(_key):
    key = _key.upper()
    out = []
    rem = list(string.ascii_uppercase)
    for i in key:
        if i in rem:
            rem.remove(i)
            out.append(i)
    out.extend(rem)
    return "".join(out)

def decipher(cph, key):
    out = []
    for ch in cph:
        if ch.isalpha():
            out.append(key[ord(ch.upper()) - 65])
        else:
            out.append(ch)
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    print(decipher(args.input.read(), form_key(args.input.key)))
