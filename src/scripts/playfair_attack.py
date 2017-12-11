"""
Apply the simulated annealing framework to a playfair cipher
"""

import argparse
import itertools

from sim_annealing import sim_anneal

def chunk(it, n, fv):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("--TEMP", type=float, default=20, help="SA param")
    parser.add_argument("--STEP", type=float, default=0.2, help="SA param")
    parser.add_argument("--COUNT", type=int, default=10000, help="SA param")
    parser.add_argument("--MUTATE", type=int, default=50, help="SA param")
    parser.add_argument("--PRINT-BOUND", type=float, default=2, help="SA param")
    return parser.parse_args()

def decipher(text, key):
    out = []
    indmap = {b: a for a, b in enumerate(key)}
    
    for a, b in chunk(text, 2, "x"):
        ai, bi = indmap[a], indmap[b]
        ar, br = ai // 5, bi // 5
        ac, bc = ai % 5, bi % 5

        if ar == br:
            if ac == 0:
                out.extend([key[ai + 4], key[bi - 1]])
            elif bc == 0:
                out.extend([key[ai - 1], key[bi + 4]])
            else:
                out.extend([key[ai - 1], key[bi - 1]])
        elif ac == bc:
            if ar == 0:
                out.extend([key[ai + 20], key[bi - 5]])
            elif br == 0:
                out.extend([key[ai - 5], key[bi + 20]])
            else:
                out.extend([key[ai - 5], key[bi - 5]])
        else:
            out.extend([key[5 * ar + bc], key[5 * br + ac]])
    return out

if __name__ == "__main__":
    args = get_args()
    sim_anneal(decipher, args.input.read(), args.TEMP, args.STEP, args.COUNT, args.MUTATE, args.PRINT_BOUND)
