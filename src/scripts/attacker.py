"""
Attacking a polyalphabetic affine ciphertext (this is a large superset of
ciphers which includes caesar ciphers, affine shifts, vigenere ciphers, and any
polyalphabetic affine scheme). Assumes you know the keyword length (see
iocattack). Turns out, brute-forcing the space for affine ciphers is pretty
easy ((26 ** 2) < 700). Considers distribution as an ordered 26 dimensional
vector and finds the smallest possible manhattan distance from expected
english.
"""

import re
import sys
import argparse
import string
import itertools

from collections import Counter

standard_dist = Counter({"E": .12702, "T": .09056, "A": .08167, "O": .07507, "I": .06966, "N": .06749, "S": .06327, "H": .06094, "R": .05987, "D": .04253, "L": .04025, "C": .02782, "U": .02758, "M": .02406, "W": .02360, "F": .02228, "G": .02015, "Y": .01974, "P": .01929, "B": .01492, "V": .00978, "K": .00772, "J": .00153, "X": .00150, "Q": .00095})

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("interval", type=int, help="keyword length to attack")
    parser.add_argument("--vigenere", action="store_true", help="search only vg")
    return parser.parse_args()

def lookat_interval(plain, start, step):
    return re.findall("[A-Z]", plain.upper())[start::step]

def hist_to_dist(hist):
    tt = sum(hist.values())
    return Counter({a: b / tt for a, b in hist.items()})

def rate_similarity(hist_1, hist_2, keys=string.ascii_uppercase):
    return sum(abs(hist_1[k] - hist_2[k]) for k in keys)

def af_shift(plain, a, b):
    return [chr((a * (ord(c) - 65) + b) % 26 + 65) for c in plain]

def attack_interval(plain, start, step, vigenere):
    plain_aoi = lookat_interval(plain, start, step)
    rearrs = [(af_shift(plain_aoi, a, b), a, b) for a in range(1, 27 if not vigenere else 2) for b in range(26)]
    rearrs = [(rate_similarity(hist_to_dist(Counter(i[0])), standard_dist), i) for i in rearrs]
    return min(rearrs)[1][1:]

def mod_inverse(a, n):
    """
    Find the modular multiplicative inverse
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    t, nt, r, nr = 0, 1, n, a
    while nr:
        quot = r // nr
        t, nt = nt, t - quot * nt
        r, nr = nr, r - quot * nr
    if r > 1:
        raise ValueError("not invertible")
    if t < 0:
        t = t + n
    return t

def invert_linear(ab):
    a, b = ab
    try:
        a = mod_inverse(a, 26)
    except ValueError:
        sys.stderr.write("inversion failed")
        return 0, 0
    b = (-b * a) % 26
    return a, b

def keyword(keys):
    if any(i[0] != 1 for i in keys):
        return ", ".join("({}/{!r}, {!r})".format(a, string.ascii_uppercase[a], string.ascii_uppercase[b]) for a, b in map(invert_linear, keys))
    else:
        return "".join(string.ascii_uppercase[-i[1]] for i in keys)

def cased_shift(ch, a, b):
    if ch.isupper():
        return chr((a * (ord(ch) - ord('A')) + b) % 26 + ord('A'))
    return chr((a * (ord(ch) - ord('a')) + b) % 26 + ord('a'))

def attack_text(plain, interval, vigenere):
    guessed_keys = [attack_interval(plain, i, interval, vigenere) for i in range(interval)]
    vals = itertools.cycle(guessed_keys)
    out = []
    for ch in plain:
        if ch.isalpha():
            out.append(cased_shift(ch, *next(vals)))
        else:
            out.append(ch)
    return "".join(out), "{} - ({})\n".format(guessed_keys, keyword(guessed_keys))

if __name__ == "__main__":
    args = get_args()
    plain = args.input.read()
    out, err = attack_text(plain, args.interval, args.vigenere)
    print(out)
    sys.stderr.write(err)
