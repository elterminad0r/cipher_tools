"""
Substitute based on letter position and word length
"""

import re
import argparse
import itertools
import pprint

from collections import defaultdict

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("table", type=argparse.FileType("r"), help="table file")
    return parser.parse_args()

def chunk(it, n, fv):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

w_or_punc = re.compile("[A-Za-z]+|[^A-Za-z]+")

def build_table(tab_file):
    tab = defaultdict(lambda: defaultdict(dict))
    _, *head = tab_file.readline().split()
    for line in tab_file:
        letter, *data = line.split()
        for name, val in zip(head, data):
            if val != "_":
                ln, pos = name.split("_")
                tab[int(ln)][int(pos)][val] = letter
    return tab

def transform_text(text, table):
    out = []
    for word, punc in chunk(w_or_punc.findall(text), 2, fv="."):
        word_tab = table[len(word)]
        nout = []
        for pos, ch in enumerate(word):
            nout.append(word_tab[pos].get(ch, ch))
        out.append("".join(nout))
        out.append(punc)
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    table = build_table(args.table)
    print("read table")
    pprint.pprint(table)
    print(transform_text(args.input.read(), table))
