#!/usr/bin/env python3

"""
Transpose a text like a matrix. Supports transposing by newlines, or explicitly
given a block length
"""

import sys
import argparse
import itertools

from strip_stdin import strip

def chunk(it, n):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=" ")

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-l", "--length", type=int,
                                    help="explicit block length")
    return parser.parse_args()

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    args = parse_args()
    if not args.length:
        print("\n".join(map("".join, zip(*map(str.split, sys.stdin)))))
    else:
        print("\n".join(map("".join, zip(*chunk(strip(sys.stdin.read()), args.length)))))
