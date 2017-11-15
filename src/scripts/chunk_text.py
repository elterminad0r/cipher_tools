"""
Splitting text into chunks (a la polybius)
"""

import re
import sys
import string
import argparse

acc_codex = string.ascii_uppercase + string.digits

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chunk", default=2, type=int,
                                    help="chunk length")
    parser.add_argument("-a", "--accumulate", action="store_true",
                                    help="accumulate chunks into single characters")
    return parser.parse_args()

def chunk(it, n):
    return zip(*[iter(it)] * n)

def accumulate_chars(plain, chunk_length):
    combs = {}
    for a in map("".join, chunk(plain, chunk_length)):
        if a not in combs:
            combs[a] = len(combs)
        sys.stdout.write(acc_codex[combs[a]])

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    args = parse_args()
    plain = sys.stdin.read()
    if args.accumulate:
        accumulate_chars(plain, args.chunk)
    else:
        print(" ".join(map("".join, chunk(plain, args.chunk))))
