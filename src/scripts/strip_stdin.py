#!/usr/bin/env python3

"""
Strip all non-alpha characters from a text. This can be used eg to remove the
spaces from blocked text.
"""

import sys
import re
import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    return parser.parse_args()

def strip(plain):
    return "".join(re.findall("[a-zA-Z]", plain))

if __name__ == "__main__":
    args = get_args()
    sys.stdout.write(strip(args.input.read()))
