#!/usr/bin/env python3

"""
Perform frequency analysis on text. This is already provided by !f, this script
exists for other reasons.
"""

import sys
import argparse
import re

from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", type=int, default=1,
                                    help="Vigenere-style key length")
    return parser.parse_args()

def IOC(cnt):
    total = sum(cnt.values())
    if total:
        return (sum(freq ** 2 - freq for freq in cnt.values())
             / (total ** 2 - total))
    else:
        return -1

def printchart(hist, start, interval, width=80):
    (_, highest), = hist.most_common(1)
    highw = len(str(highest))
    return ("IOC {:.4f}\nInterval [{}::{}]\n{}"
                    .format(IOC(hist), start, interval,
                           ("\n".join("{!r} ({:{highw}}) {}"
                                .format(letter, frequency,
                                "-" * int(width * frequency / highest),
                                highw=highw)
                                    for letter, frequency in hist.most_common()))))

def histogram(text, start, interval):
    return Counter(re.findall("[a-zA-Z]", text)[start::interval])

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command line script requiring stdin")
    args = parse_args()
    plain = sys.stdin.read()
    for i in range(args.length):
        print(printchart(histogram(plain, i, args.length), i, args.length))
