#!/usr/bin/env python3

"""
Form columns from text, preserving puncutation. If you suspect you're dealing
with a polyalphabetic cipher, you might use this to gain some insight. Takes
one argument, which is number of columns.
"""

import sys
import argparse
import re
import itertools

def chunk(it, n):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=" ")

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("cols", type=int,
                            help="number of columns")
    return parser.parse_args()

def format_cols(text, cols):
    text = re.sub(r"\s+", " ", text)
    runs = []
    for run in re.findall(r"[^a-zA-Z]+|[a-zA-Z]+", text):
        if run.isalpha():
            runs.extend("_".join(run))
        else:
            runs.append(run)
    longest_punc = max(map(len, runs))
    runs = [i if i != "_" else i * longest_punc for i in runs]
    out = []
    for row in chunk(runs, cols * 2):
        for ltr, pnc in chunk(row, 2):
            out.append("{}{:{}}".format(ltr, pnc, longest_punc))
        out.append("\n")
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    print(format_cols(args.input.read(), args.cols))
