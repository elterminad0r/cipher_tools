import sys
from collections import defaultdict

class PrefixTree:
    def __init__(self):
        self.children = defaultdict(PrefixTree)
        self.is_end = False

    def add_word(self, word):
        if word:
            start, *word = word
            self.children[start].add_word(word)
        else:
            self.is_end = True

    def __repr__(self):
        return "PrefixTree(end={!r}, children={!r})".format(self.is_end, self.children)

    def longest_word_from(self, lst, pos):
        if pos < len(lst):
            it = lst[pos]
            if it in self.children:
                ch_res = self.children[it].longest_word_from(lst, pos + 1)
                if ch_res is not None:
                    return 1 + ch_res
            if self.is_end:
                return 0

def build_pt():
    pt = PrefixTree()
    with open("data/words") as wordfile:
        for word in wordfile:
            pt.add_word(word.strip().lower())
    return pt

def split_words(pt, st):
    chs = list(st.lower())
    pos = 0
    while pos < len(st) - 1:
        nxt = pt.longest_word_from(chs, pos)
        yield "".join(chs[pos:pos + nxt])
        pos += nxt

if __name__ == "__main__":
    pt = build_pt()
    for word in split_words(pt, sys.stdin.read()):
        print("{} ".format(word), end="")
