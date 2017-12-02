"""
Report on bigram frequencies
"""

import re
import itertools
import argparse

from collections import Counter

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("-n", type=int, default=2, help="length to analyse (2 by default)")
    parser.add_argument("-t", type=int, default=20, help="total items to print")
    return parser.parse_args()

def chunk(text, n):
    return itertools.zip_longest(*[iter(text)] * n, fillvalue=" ")

def bigrams(text, n, total):
    out = []
    bgs = Counter(map("".join, chunk(re.findall("[A-Za-z]", text), n)))
    if n == 2 and not any(a == b for a, b in bgs.keys()):
        out.append("**NO IDENTICAL DOUBLES")
    (_, most), = bgs.most_common(1)
    out.append("\n".join("{} ({:{m}}): {}".format(item, count, "\u2796" * int(count * 80 / most), m=len(str(most)))
                                    for item, count in bgs.most_common(total)))
    return "\n".join(out)

if __name__ == "__main__":
    args = get_args()
    print(bigrams(args.input.read(), args.n, args.t))
