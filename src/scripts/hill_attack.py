"""
Cryptanalysis of an arbitrary size Hilll cipher given a likely crib substring
"""

import sys
import argparse
import re
import itertools
import string

from collections import deque

from hill_encipher import letters

try:
    import sympy
except ImportError:
    sys.exit("this script is dependent on SymPy")

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("size", type=int, help="size of encryption matrix")
    parser.add_argument("crib", type=str,
                                    help="likely crib substring to attack")
    args = parser.parse_args()
    if args.size < 2:
        parser.error("size should be > 2")
    args.crib = "".join(re.findall("[a-z]", args.crib.lower()))
    if len(args.crib) < args.size * (args.size + 1) - 1:
        parser.error("crib should be composed of letters and have at least {}".format(args.size * (args.size + 1) - 1))
    return args

def chunk(it, n, fv=None):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def roll(_it, n):
    it = iter(_it)
    window = deque(next(it) for _ in range(n))
    yield window
    for i in it:
        window.append(i)
        window.popleft()
        yield window

def potential_matrices(_text, size, _crib):
    text = [ord(c.upper()) - 65 for c in _text]
    #print("text: {} {}".format(_text, text))
    cribs = [sympy.Matrix(list(zip(*chunk(i, size)))) for i in roll([ord(ch.upper()) - 65 for ch in _crib], size ** 2)]
    #print(cribs)
    slides = roll(chunk(text, size, " "), size)
    for sl in slides:
        try:
            #print(sl)
            inverted = sympy.Matrix(list(zip(*sl))).inv_mod(26)
            for crib in cribs:
                #print(sl, inverted, crib)
                yield crib * inverted
        except ValueError:
            pass

def decipher(text, mat, size):
    out = []
    for chnk in chunk([ord(ch.upper()) - 65 for ch in text], size, 0):
        out.extend(string.ascii_uppercase[i % 26] for i in mat * sympy.Matrix(chnk))
    return "".join(out)

def attack(text, size, crib):
    text = "".join(text)
    for mat in potential_matrices(text, size, crib):
        print(decipher(text, mat, size))

if __name__ == "__main__":
    args = get_args()
    print(attack(letters(args.input.read()), args.size, args.crib))
