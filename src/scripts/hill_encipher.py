"""
Hill enciphering
"""

import sys
import argparse
import string
import itertools

try:
    import sympy
except ImportError:
    sys.exit("this script requires SymPy")

def chunk(it, n, fv=None):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def letters(t):
    return filter(str.isalpha, t)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("size", type=int, help="matrix size")
    parser.add_argument("-m", "--mat", nargs="+", required=True, type=int, help="the matrix")
    return parser.parse_args()

def hill_encipher(text, mat):
    out = []
    for pair in chunk((ord(ch.upper()) - 65 for ch in text), 2, 0):
        out.extend(string.ascii_uppercase[i % 26] for i in mat * sympy.Matrix(pair))
    return "".join(out)

if __name__ == "__main__":
    args = get_args()
    print(hill_encipher(letters(args.input.read()), sympy.Matrix(list(chunk(args.mat, args.size)))))
