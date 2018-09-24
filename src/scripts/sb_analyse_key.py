"""
Perform some analysis of a substitution cipher key
"""

import argparse

from hill_brute import text_as_ints

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("key", type=str, nargs="*", help="the key to analyse")
    return parser.parse_args()

def visualise(key):
    print(key)
    print()
    print("\n".join("{}: {}".format(ch, "\u2500" * (ord(ch.upper()) - 65) * 2) for ch in key))
    i_rep = text_as_ints(key)
    print()
    print(i_rep)
    print()
    print([(-i_rep[i] + i_rep[i + 1]) % 26 for i in range(len(i_rep) - 1)])

if __name__ == "__main__":
    args = get_args()
    visualise(args.key[-1])
