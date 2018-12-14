"""
Decipher a substitution cipher
"""

import sys
import argparse
import string

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("key", type=str, help="the key")
    parser.add_argument("--late", action="store_true",
                        help="pad with late alphabet chars")
    return parser.parse_args()

def form_key(_key, resume_late=False):
    key = _key.upper()
    out = []
    rem = list(string.ascii_uppercase)
    for i in key:
        if i in rem:
            rem.remove(i)
            out.append(i)
    if not resume_late:
        out.extend(rem)
    else:
        largest = max(key)
        resume_idx = len(rem)
        while resume_idx >= 0:
            if rem[resume_idx - 1] < largest:
                break
            resume_idx -= 1
        out.extend(rem[resume_idx:])
        out.extend(rem[:resume_idx])
    return invert_key("".join(out))

def invert_key(_key):
    key = _key.upper()
    dct = {c: ind for ind, c in enumerate(key)}
    return "".join(string.ascii_uppercase[dct[string.ascii_uppercase[i]]]
                   for i in range(26))

def decipher(cph, key):
    print("key: {!r}".format(key), file=sys.stderr)
    out = []
    for ch in cph:
        if ch.isalpha():
            out.append(key[ord(ch.upper()) - 65])
        else:
            out.append(ch)
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    print(decipher(args.input.read(), form_key(args.key, args.late)))
