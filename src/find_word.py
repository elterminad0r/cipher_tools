#!/usr/bin/env python3

"""
A script that searches for possible words matching a prototype. Designed such
that plaintext from a substitution ciphertext can be pasted in. Characters are
considered as equality classes, and are anonymous apart from just which others
they correspond to. Also supports absolute references to characters, by
backslash escaping. The actual word-finding processed uses no regex, just lists
of which character indices should coincide with others. It brute-forces through
a copy of /usr/share/dict/words (as I can't rely on anyone in this cruel word
having the moral integrity to use linux)
"""

################################################################################

import re
import os
import sys

from collections import defaultdict

# matching a letter atom, which has an optional backslash
letter = re.compile(r"\\?.")

def build_match(pattern):
    """
    Parse a supplied pattern given as a string. Return a list of lists of
    indices which should coincide, alongside a list of directly known
    characters.
    """
    # defaultdict to dynamically generate required lists
    groups = defaultdict(list)
    # must be set to number of actual letter atoms
    known = [None for _ in letter.findall(pattern)]
    ind = 0
    for ind, ch in enumerate(letter.findall(pattern)):
        # handling an absolute atom
        if ch.startswith("\\"):
            known[ind] = ch[1].lower()
        # adding a nonabsolute atom to its corresponding list
        else:
            groups[ch].append(ind)

    # just return the values in the dict, keys have served their purpose
    return groups.values(), known

def matches(match, known, word, length):
    """
    Check if a word matches a pattern infrastructure. Takes absolute
    characters, groups, and target length as arguments.
    """
            # first check if it's the right length as further checks make this
            # assumption
    return (len(word) == length and
          # check if all absolute values are correct
          all(word[ind] == ch
                for ind, ch in enumerate(known) if ch is not None) and
          # check if all identity groups are correct
          all(len(set(word[i] for i in group)) == 1
                for group in match) and
          # check if all identity groups have different chars
          len(set(word[group[0]] for group in match)) == len(match))

def find_matches(pattern):
    """
    Brute force through the english dictionary in search of words matching a
    pattern
    """
    match, known = build_match(pattern)
    l = len(known)
    # open local copy of /usr/share/dict/words
    with open(os.path.join(os.path.dirname(__file__),
              "data/words"),
             "r") as word_file:
        return "\n".join(word for word in map(str.strip, word_file)
                                if matches(match, known, word.lower(), l))

# if called directly, pattern search (optionally read pattern from argv)
if __name__ == "__main__":
    # cheeky truthiness test
    if len(sys.argv) - 1:
        patt = sys.argv[1]
    else:
        patt = input("Enter the pattern of letters you'd like to look for > ")
    print(find_matches(patt))
