"""
Preprocess text into a network of words suitable for processing by a clustering
algorithm
"""

import re
import argparse
import itertools

from collections import defaultdict

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("--bound", type=int, default=4)
    parser.add_argument("--fracbound", type=float, default=0.49)
    return parser.parse_args()

def hamming(a, b):
    return sum(a != b for a, b in zip(a, b))

def words(text):
    return re.findall("[A-Z]+", text.upper())

def process_words(words, bound, fracbound):
    ln_groups = defaultdict(list)
    for w_pos, w in enumerate(words):
        ln_groups[len(w)].append((w, "{}_{}".format(w, w_pos)))

    for ln, group in ln_groups.items():
        for (a, a_name), (b, b_name) in itertools.combinations(group, 2):
            dst = hamming(a, b)
            if dst < bound and dst / ln < fracbound:
                print("{}\t{}\t{}".format(a_name, b_name, ln-dst))

if __name__ == "__main__":
    args = get_args()
    process_words(words(args.input.read()), args.bound, args.fracbound)
