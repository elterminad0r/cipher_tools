"""
Decipher playfair given plaintext
"""

import re
import argparse
import string

from bifid_attack import getdeciph
from hill_brute import text_as_ints

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("key", type=str, help="bifid key")
    parser.add_argument("period", type=int, help="bifid period")
    return parser.parse_args()

def fmstring(text):
    return re.sub(r"[a-zA-Z]", "{}", text)

def show_plain(cph, key, period):
    dcph = getdeciph(period)(*map(text_as_ints, [cph, key]))
    print(fmstring(cph).format(*(string.ascii_uppercase[i] for i in dcph)))

def form_key(_key):
    key = _key.upper()
    out = []
    rem = list(string.ascii_uppercase)
    rem.remove("J")
    for i in key:
        if i in rem:
            rem.remove(i)
            out.append(i)
    out.extend(rem)
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    show_plain(args.input.read(), form_key(args.key), args.period)
