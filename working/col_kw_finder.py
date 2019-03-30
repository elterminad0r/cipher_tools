#!/usr/bin/env python3.7

"""
Finding words that match a columnar transposition key in a set of candidates.
"""

import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--word-file", type=argparse.FileType("r"), default="-",
        help="a text file which will be used to find candidate words")
    parser.add_argument(
        "--verbose", action="store_true",
        help="print candidates")
    parser.add_argument(
        "--disregard-spaces", action="store_true",
        help="take every compatible substring")
    parser.add_argument(
        "--discriminate", action="store_true",
        help="if using spaces, preselect candidates to have the correct length")
    parser.add_argument(
        "--clobber", action="store_true",
        help="instead of acting normally, clobber repeated letters")
    parser.add_argument(
        "target",
        help="a congruent key to the key that was used")
    return parser.parse_args()

def rolling_chunk(ls, n):
    return [ls[i:i + n] for i in range(len(ls) - n + 1)]

def remove_repeated(w):
    # only guaranteed to work in Python 3.7 as dicts preserve insertion order in
    # the language spec. Should also work in CPython 3.6 but implementation
    # detail
    return "".join(dict.fromkeys(w))

def get_words(plaintext, keyword, disregard_spaces, discriminate):
    if not disregard_spaces:
        if discriminate:
            yield from set(i for i in map(str.upper,
                               "".join(
                                filter(lambda s: s.isalpha() or s.isspace(),
                                       plaintext)).split())
                           if len(i) == len(keyword))
        else:
            yield from set(i for i in map(str.upper,
                               "".join(
                                filter(lambda s: s.isalpha() or s.isspace(),
                                       plaintext)).split()))
    else:
        yield from map("".join,
                       rolling_chunk(list(filter(str.isalpha, plaintext)),
                                     len(keyword)))

def construct_key(keyword, clobber):
    if clobber:
        keyword = remove_repeated(keyword)
    enumd = list(enumerate(keyword))
    enumd.sort(key = lambda x: x[1])
    key = [None] * len(keyword)
    for ind, (orig_ind, _) in enumerate(enumd):
        key[orig_ind] = ind
    return key

def find_match(keyword, plaintext, verbose, disregard_spaces, clobber,
               discriminate):
    key = construct_key(keyword, clobber)
    results = []
    for candidate in get_words(plaintext, keyword, disregard_spaces,
                               discriminate):
        cand_key = construct_key(candidate, clobber)
        if args.verbose:
            print("candidate: {} {}".format(candidate,
                        "".join(map(str, cand_key))))
        if cand_key == key:
            print(candidate)
            results.append(candidate)
    print(results)

if __name__ == "__main__":
    args = get_args()
    find_match(args.target, args.word_file.read(), args.verbose,
               args.disregard_spaces, args.clobber, args.discriminate)
