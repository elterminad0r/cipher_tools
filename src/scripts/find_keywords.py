#!/usr/bin/env python3

"""
Find all runs of words ("phrases") occurring in stdin with a certain length.
(might be used to search for a keyword or name)
"""

import sys
import re
import argparse

from collections import deque

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("length", type=int, help="phrase length")

def stream_into_words(wd_file):
    return re.findall("[a-z]+", re.sub("[^a-zA-Z ]", " ", wd_file.read()), re.I)

def find_keys(length, _words):
    words = iter(_words)
    pool = deque()
    try:
        while True:
            while sum(map(len, pool)) < length:
                pool.append(next(words))
            while sum(map(len, pool)) > length:
                pool.popleft()
            if sum(map(len, pool)) == length:
                yield pool.copy()
                pool.popleft()
    except StopIteration:
        pass

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    args = get_args()
    for k in find_keys(args.length, stream_into_words(sys.stdin)):
        print(" ".join(k))
