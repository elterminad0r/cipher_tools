#!/usr/bin/env python3

"""
Reverse text. Can retain or strip punctuation, and also not reverse
punctuation, with -s and -r respectively.
"""

import sys
import re
import argparse

from strip_stdin import strip

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("-s", "--strip-punc", action="store_true",
                                help="strip punctuation in process")
    actions.add_argument("-r", "--rev-retain", action="store_true",
                                help="do not reverse punctuation")
    return parser.parse_args()

def build_template(text):
    return re.sub("[a-zA-Z]", "{}", text)

def rev_text(text):
    return build_template(text).format(*reversed(re.findall("[a-zA-Z]", text)))

if __name__ == "__main__":
    args = parse_args()
    plain = args.input.read().strip()
    if args.strip_punc:
        print(strip(plain)[::-1])
    elif args.rev_retain:
        print(rev_text(plain))
    else:
        print(plain[::-1])
