#!/usr/bin/env python3

"""
Utility/convenience script to perform heuristic splitting on dense text. Uses a
prefix tree for *very* fast lookups. Using PyPy, you can cut the initialisation
stage from around 0.736s to 0.487s (around 51.13%).
"""

import sys
import argparse
import textwrap
import string
import time

from collections import defaultdict

letter_set = set(string.ascii_lowercase + "_")

def strip_punc(word):
    """
    Strip punctuation from word
    """
    return "".join(ch for ch in word.lower() if ch in letter_set)

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--dump", action="store_true",
                            help="pprint a tree dump")
    parser.add_argument("--nltk", action="store_true",
                            help="use nltk word corpus")
    return parser.parse_args()

class PrefixTree:
    """
    A prefix tree class that can be used to quickly find a word in a set of
    characters.
    """
    def __init__(self):
        # the dictionary of children - automatically create new tree when
        # needed
        self.children = defaultdict(PrefixTree)
        # track if this tree represents the end of a known word
        self.is_end = False

    # add a word to the tree, using recursive haskell-esque style
    def add_word(self, word, pos=0):
        if pos < len(word):
            # get first character and remainder, add to child
            self.children[word[pos]].add_word(word, pos + 1)
        else:
            # if the word is empty, this is the end node
            self.is_end = True

    # remove word from tree, by unsetting flag
    def remove_word(self, word, pos=0):
        # if this is the end node of this word
        if pos == len(word):
            self.is_end = False
        # delegate to child nodes
        else:
            self.children[word[pos]].remove_word(word, pos + 1)

    # easy repr of tree
    def __repr__(self):
        return "PrefixTree(end={!r}, children={!r})".format(self.is_end, self.children)

    # a slightly more tree-like representation of the tree
    def __str__(self):
        return textwrap.indent(
                        "\n".join(
                            "└{}─{}".format(k, str(v).lstrip())
                                    for k, v in self.children.items()),
                        "  ")

    # get the longest word you can find from a point in a collection of
    # characters. returns length of next word.
    def longest_word_from(self, chars, pos):
        # if the position is within bounds
        if pos < len(chars):
            # get the character to inspect
            currchar = chars[pos]
            # check if any space-overloaded words are known
            space_res = ""
            if self.is_end:
                space_res = " {}".format(self.children["_"].longest_word_from(chars, pos) or "").rstrip()
            # try to obtain a result from children (the longest possible word)
            if currchar in self.children:
                child_result = self.children[currchar].longest_word_from(chars, pos + 1)
                if child_result is not None:
                    return max("{}{}".format(currchar, child_result),
                               space_res,
                               key=len)
                if space_res != "":
                    return space_res
            if self.is_end:
                return ""

def build_pt(args):
    """
    Build a prefix tree from data/words (local copy of /usr/share/dict/words
    """
    preftree = PrefixTree()

    # build tree from words
    try:
        if not args.nltk:
            print("not using nltk")
            raise ImportError
        print("trying to use nltk")
        import nltk
    except ImportError:
        print("final not using")
        with open("data/words") as wordfile:
            for word in map(strip_punc, wordfile):
                preftree.add_word(word)
    else:
        print("using nltk")
        for word in nltk.corpus.words.words():
            preftree.add_word(word)

    # special cased words, includes extra, deletions and space overloading
    with open("data/extra_words") as extrafile:
        for word in filter(None, map(str.lower, map(str.strip, extrafile))):
            if not word.startswith("#"):
                if word.startswith("^"):
                    preftree.remove_word(word, 1)
                else:
                    preftree.add_word(word, 0)
    return preftree

def split_words(preftree, dense_str):
    """
    Split words from dense string into separate words
    """
    made_lower = dense_str.lower()
    pos = 0
    while pos < len(dense_str) - 1:
        nxt = preftree.longest_word_from(made_lower, pos)
        yield nxt
        pos += len(strip_punc(nxt))

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command line script that requires STDIN")
    args = parse_args()
    start = time.time()
    print("initialising..")
    preftree = build_pt(args)
    print("initialised (took {:.3f} secs)".format(time.time() - start))
    if not args.dump:
        for word in split_words(preftree, sys.stdin.read()):
            print("{} ".format(word), end="")
        print()
    else:
        print(preftree)
