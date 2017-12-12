"""
Calculate variances of bigrams with certain 'steps' as per
http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-bifid-cipher/
"""

import argparse

from collections import Counter

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"),
                                    help="input file")
    parser.add_argument("--range", type=int, default=20,
                                    help="number of steps to check")
    parser.add_argument("--factor", type=int, default=5, help="stretch factor in graph")
    return parser.parse_args()

def variance(counts):
    mean = sum(counts) / len(counts)
    return sum((i - mean) ** 2 for i in counts) / len(counts)

def showvars(text, maxrange, stretch):
    out = []
    text = "".join(filter(str.isalpha, text))
    for offs in range(1, maxrange):
        var = variance(Counter((text[i], text[i + offs]) for i in range(len(text) - offs)).values())
        out.append("{:2} ({:6.3f}): {}".format(offs, var, "\u2796" * int(stretch * var)))
    return "\n".join(out)

if __name__ == "__main__":
    args = get_args()
    print(showvars(args.input.read(), args.range, args.factor))
