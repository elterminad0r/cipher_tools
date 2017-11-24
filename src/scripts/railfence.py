#!/usr/bin/env python3

"""
Utility script to undo a rail fence cipher. Takes an optional argument -r which
is number of rails.
"""

import itertools
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-r", "--rail", type=int, default=3,
                                help="number of rails")
    return parser.parse_args()

def chunk(it, n):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=" ")

def railfence(plain, rails):
    cycle_length = 2 * rails - 2
    width = len(plain) // cycle_length
    cycle_starts, plain = [[i] for i in plain[:width + 1]], plain[width + 1:]
    cycle_ends, plain = [[i] for i in plain[-width:]], plain[:-width]
    for _ in range(rails - 2):
        row, plain = plain[:width * 2], plain[width * 2:]
        for ind, (a, b) in enumerate(chunk(row, 2)):
            cycle_starts[ind].append(a)
            cycle_ends[ind].append(b)
    return "".join("{}{}".format(*map("".join, [a, b])) for a, b in itertools.zip_longest(cycle_starts, cycle_ends, fillvalue=[" "]))

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    args = parse_args()
    plain = sys.stdin.read().strip()
    print(railfence(plain, args.rail))
