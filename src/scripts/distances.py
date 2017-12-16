"""
distances between substrings
"""

import argparse
import re
import pprint
import sympy

def letters(text):
    return "".join(re.findall(r"[A-Za-z]", text))

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input")
    parser.add_argument("substring", type=str, help="substring")
    return parser.parse_args()

def dists(text, sub):
    out = []
    first = text.find(sub)
    text = text[first:]
    while text.find(sub, 1) != -1:
        pos = text.find(sub, 1)
        out.append(text[:pos])
        text = text[pos:]
    return out

def present(chunks):
    pprint.pprint(chunks)
    lengths = [len(i) for i in chunks]
    print(lengths)
    print([sympy.factorint(i) for i in lengths])

if __name__ == "__main__":
    args = get_args()
    present(dists(*map(letters, [args.input.read(), args.substring])))
