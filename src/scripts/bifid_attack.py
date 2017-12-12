"""
Apply the simulated annealing framework to a bifid cipher
"""

import argparse
import itertools
import string

from sim_annealing import sim_anneal

def chunk(it, n, fv):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("period", type=int, help="bifid period")
    parser.add_argument("--TEMP", type=float, default=20, help="SA param")
    parser.add_argument("--STEP", type=float, default=0.1, help="SA param")
    parser.add_argument("--COUNT", type=int, default=10000, help="SA param")
    parser.add_argument("--MUTATE", type=int, default=50, help="SA param")
    parser.add_argument("--PRINT-BOUND", type=float, default=2, help="SA param")
    return parser.parse_args()

def getdeciph(period):
    def decipher(text, key):
        result = []
        for i in range(0, len(text), period):
            nxt = period
            if i + period >= len(text):
                text += [25] * (len(text) - i)
            for j in range(nxt):
                a = text[i + (j // 2)]
                b = text[i + ((period + j) // 2)]

                ai = key.index(a)
                bi = key.index(b)
                ar = ai // 5
                br = bi // 5
                ac = ai % 5
                bc = bi % 5
                if j % 2 == 0:
                    result.append(key[5 * ar + br])
                else:
                    result.append(key[5 * ac + bc])
        return result
    return decipher

if __name__ == "__main__":
    args = get_args()
    sim_anneal(getdeciph(args.period), args.input.read(), args.TEMP, args.STEP, args.COUNT, args.MUTATE, args.PRINT_BOUND)
