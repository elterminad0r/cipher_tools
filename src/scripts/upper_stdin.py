#!/usr/bin/env python3

"""
Modify the casing of text
"""

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-l", "--lower", action="store_true",
                                help="make text lowercase rather than uppercase")
    return parser.parse_args()

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("this is a command line script")
    args = parse_args()
    if args.lower:
        sys.stdout.write(sys.stdin.read().lower())
    else:
        sys.stdout.write(sys.stdin.read().upper())
