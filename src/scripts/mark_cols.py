"""
Mark polyalphabetic columns in text
"""

import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
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
    if sys.stdin.isatty():
        sys.exit("This is a command line script requiring stdin")
    args = get_args()
    display_intervals(sys.stdin.read(), args.length, args.interval)
