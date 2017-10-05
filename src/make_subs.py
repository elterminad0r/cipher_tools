#!/usr/bin/env python3

"""
Making substitutions to a source text. Assumes source text is case
insensitive/capcased, and substitution should be performed on alphabetic
characters.
"""

################################################################################

import sys
import re

from input_handling import read_file

sub_pattern = re.compile(r"\b[A-Z][a-z]\b")

def parse_subs(subs):
    print("extracted pairs: {}".format(sub_pattern.findall(subs)))
    return dict(sub_pattern.findall(subs))

def _make_subs(source, subs):
    for ch in source:
        yield subs.get(ch, ch)

def make_subs(source, subs):
    return "".join(_make_subs(source, subs))

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
