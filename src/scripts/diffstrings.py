"""
Show difference between strings
"""

import string
import argparse
import re

def letters(text):
    return re.findall("[A-Za-z]", text)

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=str)
    parser.add_argument("b", type=str)
    return parser.parse_args()

def diff(a, b):
    for x, y in zip(a, b):
        x, y = map(lambda c: ord(c.upper()) - 65, (x, y))
        d = x - y
        print("{} {}".format(string.ascii_uppercase[d], string.ascii_uppercase[-d]))

if __name__ == "__main__":
    args = parse_args()
    diff(args.a, args.b)
