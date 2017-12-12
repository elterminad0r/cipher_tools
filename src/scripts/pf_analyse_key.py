"""
Analyse a stochastically generated playfair key, using vim-like keybindings to
shift the key.
"""

import argparse
import itertools

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("key", type=str, help="pf key to analyse")
    return parser.parse_args()

def form_key(key):
    return list(zip(*[iter(key)] * 5))

def print_key(key):
    print("\n".join(map(" ".join, key)))
    print("".join(itertools.chain.from_iterable(key)))

def shift_rows(key, n):
    return key[n:] + key[:n]

def shift_cols(key, n):
    return [row[n:] + row[:n] for row in key]

print(shift_rows(list(range(25)), 5))

ACTIONS = {"j": lambda key: shift_rows(key, -1),
           "k": lambda key: shift_rows(key, 1),
           "l": lambda key: shift_cols(key, -1),
           "h": lambda key: shift_cols(key, 1)}

def play(_key):
    assert len(_key) == 25
    key = form_key(_key)
    while True:
        print_key(key)
        act = input("> ")
        if act in ACTIONS:
            print("success")
            key = ACTIONS[act](key)
            print(key)
        else:
            print("unrecognised")

if __name__ == "__main__":
    args = get_args()
    play(args.key)
