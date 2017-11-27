#!/usr/bin/env python3

"""
Mark polyalphabetic columns in text. This does not actually show the columns as
columns, but provides inline markers (can be used to find interval to make
substitutions)
"""

import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("length", type=int,
                            help="total column length")
    parser.add_argument("interval", type=int,
                            help="sub intervals")
    return parser.parse_args()

def display_intervals(text, length, interval):
    lcount = 1
    icount = interval
    for c in text:
        if c.isalpha():
            lcount -= 1
            icount -= 1
        if not lcount:
            sys.stdout.write("^")
            lcount = length
            icount = interval
        elif not icount:
            sys.stdout.write("|")
            icount = interval
        sys.stdout.write(c)

if __name__ == "__main__":
    args = get_args()
    display_intervals(args.input.read(), args.length, args.interval)
