#!/usr/bin/env python3

"""
Making substitutions to a source text. Assumes source text is case
insensitive/capcased, and substitution should be performed on alphabetic
characters.
"""

################################################################################

import sys
import re
import shlex

import string

from input_handling import read_file

alpha_set = set(string.ascii_letters)

def parse_subs(subs):
    out = {}
    for pair in shlex.split(subs):
        if len(pair) != 2:
            raise ValueError("Non-pair encountered: {}".format(pair))
        k, v = pair
        out[k] = v
    return out

def _make_subs(source, subs):
    for ch in source:
        yield subs.get(ch, ch)

def _alt_subs(source, subs):
    for ch in source:
        if ch in subs:
            yield "\\{}".format(subs[ch])
        else:
            yield ch

def _under_subs(source, subs):
    for ch in source:
        if ch in subs:
            yield subs[ch]
        elif ch in alpha_set:
            yield "_"
        else:
            yield "({})".format(ch)

def make_subs(source, subs, generator=_make_subs):
    return "".join(generator(source, subs))

def tty_subs():
    return parse_subs(input("Enter substitutions > "))

def pretty_subs(subs):
    return "{}\n{}".format(
                    " ".join("{}{}".format(*kv) for kv in subs.items()),
                    "\n".join("{} -> {}".format(*kv) for kv in subs.items()))

if __name__ == "__main__":
    if not sys.stdin.isatty():
        sys.exit("stdin must be tty for direct sub mode")

    source = read_file()
    print("The given source was:\n{}".format(source))
    subs = {}

    while True:
        print("\n\n")
        subs.update(tty_subs())
        print("Current subtable is:\n{}\n".format(pretty_subs(subs)))
        print("Resulting in source:\n{}\n".format(make_subs(source, subs)))
