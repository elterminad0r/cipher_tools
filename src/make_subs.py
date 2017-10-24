#!/usr/bin/env python3

"""
Making and parsing substitutions on a source. Makes very few assumptions about
the nature of the text - you could substitute spaces for commas if you really
wanted. Generally follows the elsewhere documented convention of shlex-split
doubles of characters.
"""

################################################################################

import sys
import re
import shlex
import itertools
import string

from input_handling import read_file

# set for letter membership testing. Used in a display hook elsewhere
alpha_set = set(string.ascii_letters)

def parse_subs(subs):
    """
    Parse shlex-like subs into dictionary
    """
    out = {}
    args = shlex.split(subs)

    for pair in args:
        if len(pair) != 2:
            raise ValueError("Non-pair encountered: {}".format(pair))
        k, v = pair
        out[k] = v
    return out

def _make_subs(source, subs):
    """
    Default display hook for subs - if a ciphertext key is not found in the
    table, just leave it as is. It does make the assumption that keys are
    alphabetical, which means it can cycle on punctuation.
    """
    inf_subs = itertools.cycle(subs)
    for ch in source:
        if ch in alpha_set:
            yield next(inf_subs).get(ch, ch)
        else:
            yield ch

def _alt_subs(source, subs):
    """
    Alternative display hook where substitutions are made explicit by a
    backslash. Can be useful if there's ambiguity.
    """
    for ch, subtable in zip(source, itertools.cycle(subs)):
        if ch in subtable:
            yield "\\{}".format(subtable[ch])
        else:
            yield ch

def _under_subs(source, subs):
    """
    Alternative where only subtitutions and backslashes are displayed (and
    parenthesised special characters). Can be useful to try and get a better
    look at words without the distraction of stray ciphertext
    """
    for ch, subtable in zip(source, itertools.cycle(subs)):
        if ch in subtable:
            yield subtable[ch]
        elif ch in alpha_set:
            yield "_"
        else:
            yield "({})".format(ch)

def make_subs(source, subs, generator=_make_subs):
    """
    Short function to join together a source with a hook, as all hooks are
    generators for simplicity
    """
    return "".join(generator(source, subs))

def tty_subs():
    """
    Read substitutions from stdin tty
    """
    return parse_subs(input("Enter substitutions > "))

def pretty_subs(subs):
    """
    Prettify a subtable. Returns both a "pastable" version and a pretty, arrow
    based version. Sorts table into alphabetical order.
    """
    return "{}\n{}".format(
                    " ".join(shlex.quote("{}{}".format(*kv))
                        for kv in sorted(subs.items())),
                    "\n".join("{} -> {}".format(*kv)
                        for kv in sorted(subs.items())))

# if called as main script, perform substitutions
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
