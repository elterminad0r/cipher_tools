"""
Apply the simulated annealing framework to a bifid cipher
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
    parser.add_argument("--STEP", type=float, default=0.1, help="SA param")
    parser.add_argument("--COUNT", type=int, default=10000, help="SA param")
    parser.add_argument("--MUTATE", type=int, default=50, help="SA param")
    parser.add_argument("--PRINT-BOUND", type=float, default=2, help="SA param")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    sim_anneal(decipher, args.input.read(), args.TEMP, args.STEP, args.COUNT, args.MUTATE, args.PRINT_BOUND)
