#!/usr/bin/env python3

"""
Transpose a text like a matrix. Supports transposing by newlines, or explicitly
given a block length
"""

import sys
import re
import argparse
import itertools

from strip_stdin import strip

def chunk(it, n):
    plen = len(it) // n
    extra = len(it) % n
    it = iter(it)
    for i in range(extra):
        yield list(itertools.islice(it, plen + 1))
    for i in range(extra, n):
        yield list(itertools.islice(it, plen))

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("-l", "--length", type=int,
                                    help="explicit block length")
    return parser.parse_args()

def scyt(mat):
    return "\n".join(map("".join, itertools.zip_longest(*mat, fillvalue=" ")))

def letters(st):
    return re.findall("[a-zA-Z]", st)

if __name__ == "__main__":
    args = parse_args()
    if not args.length:
        print(scyt(map(letters, args.input)))
    else:
        print(scyt(chunk(strip(args.input.read()), args.length)))
