"""
Brute-force a hill cipher row by row.
"""

import sys
import re
import argparse
import itertools
import string
import heapq

from operator import mul
from collections import Counter

from attacker import hist_to_dist, standard_dist, rate_similarity

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("--size", type=int, default=2,
                                    help="side length of encryption matrix")
    return parser.parse_args()

def chunk(it, n, fv):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def vctmul(row, vct):
    return sum(map(mul, row, vct))

def partial_hill(text, size, row):
    for plain_vct in chunk(text, size, 0):
        yield string.ascii_uppercase[vctmul(row, plain_vct) % 26]

def make_formstring(text):
    return re.sub("[a-zA-Z]", "{}", text)

def hill_encrypt(text, size, mat):
    out = []
    agg = []
    for agg in chunk(text_as_ints(text), size, "z"):
        out.extend(string.ascii_uppercase[vctmul(row, agg) % 26] for row in mat)
    return make_formstring(text).format(*out)

def attack_text(text, size):
    candidates = [(partial_hill(text, size, row), row) for row in itertools.product(range(26), repeat=size)]
    candidates = [(rate_similarity(standard_dist, hist_to_dist(Counter(i))), row) for i, row in candidates]
    heapq.heapify(candidates)
    return [heapq.heappop(candidates)[1] for _ in range(size)]

def text_as_ints(text):
    return [ord(ch) - 65 for ch in text.upper() if ch.isalpha()]

if __name__ == "__main__":
    args = get_args()
    text = args.input.read()
    rows = attack_text(text_as_ints(text), args.size)
    sys.stderr.write("identified rows {}".format(rows))
    for ind, mat in enumerate(itertools.permutations(rows)):
        print("permutation {}:".format(ind))
        print(hill_encrypt(text, args.size, mat))
