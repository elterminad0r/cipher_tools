import sys
from collections import defaultdict

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
    def add_word(self, word):
        if word:
            # get first character and remainder, add to child
            start, *word = word
            self.children[start].add_word(word)
        else:
            # if the word is empty, this is the end node
            self.is_end = True

    # easy repr of tree (TODO build proper string representation)
    def __repr__(self):
        return "PrefixTree(end={!r}, children={!r})".format(self.is_end, self.children)

    # get the longest word you can find from a point in a collection of
    # characters. returns length of next word.
    def longest_word_from(self, chars, pos):
        # if the position is within bounds
        if pos < len(chars):
            # get the character to inspect
            currchar = chars[pos]
            # try to obtain a result from children (the longest possible word)
            if currchar in self.children:
                child_result = self.children[currchar].longest_word_from(chars, pos + 1)
                if child_result is not None:
                    return 1 + child_result
            # otherwise, if this itself is a valid word, return 0
            if self.is_end:
                return 0

def build_pt():
    """
    Build a prefix tree from data/words (local copy of /usr/share/dict/words
    """
    preftree = PrefixTree()
    with open("data/words") as wordfile:
        for word in wordfile:
            preftree.add_word(word.strip().lower())
    return preftree

def split_words(preftree, dense_str):
    """
    Split words from dense string into separate words
    """
    made_lower = dense_str.lower()
    pos = 0
    while pos < len(dense_str) - 1:
        nxt = preftree.longest_word_from(made_lower, pos)
        yield "".join(made_lower[pos:pos + nxt])
        pos += nxt

if __name__ == "__main__":
    preftree = build_pt()
    for word in split_words(preftree, sys.stdin.read()):
        print("{} ".format(word), end="")
    print()
