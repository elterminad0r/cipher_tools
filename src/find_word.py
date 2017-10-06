#!/usr/bin/env python3

"""
A script that searches for possible words matching a pattern
"""

################################################################################

import re
import sys

from collections import defaultdict

def build_match(pattern):
    groups = defaultdict(list)
    for ind, ch in enumerate(pattern):
        groups[ch].append(ind)
    return groups.values()

def matches(match, word, length):
    return (len(word) == length and
          all(len(set(word[i] for i in group)) == 1
                for group in match) and
          len(set(word[group[0]] for group in match)) == len(match))


def find_matches(pattern):
    match = build_match(pattern)
    l = len(pattern)
    with open("data/words", "r") as word_file:
        return "\n".join(word for word in map(str.strip, word_file)
                                        if matches(match, word.lower(), l))

if __name__ == "__main__":
    if len(sys.argv) - 1:
        patt = sys.argv[1]
    else:
        patt = input("Enter the pattern of letters you'd like to look for > ")
    print(find_matches(patt))
