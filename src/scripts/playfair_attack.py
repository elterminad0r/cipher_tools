"""
Attacking a playfair cipher by simulated annealing
"""

import argparse
import itertools
import string
import math
import random
import time

from collections import defaultdict

from hill_brute import text_as_ints
from score_text import fitness

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("--TEMP", type=float, default=20, help="SA param")
    parser.add_argument("--STEP", type=float, default=0.2, help="SA param")
    parser.add_argument("--COUNT", type=int, default=10000, help="SA param")
    parser.add_argument("--MUTATE", type=int, default=50, help="SA param")
    return parser.parse_args()

def chunk(it, n, fv):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fv)

def pf_sim_anneal(text, temp, step, count, mutate):
    start = time.time()
    text = text_as_ints(text)
    key = text_as_ints(string.ascii_uppercase.replace("J", ""))
    maxscore = float("-inf")
    for i in itertools.count():
        score, conj_key = pfcrack(text, key, temp, step, count, mutate)
        if score > maxscore:
            maxscore = score
            key = conj_key
            print("it {} yields score {}".format(i, maxscore))
            print("took {:.3f}s".format(time.time() - start))
            print("key: {}".format(key))
            print("plaintext: {}".format("".join(string.ascii_uppercase[i] for i in decipher(text, key))))
        else:
            print("no improvement at iteration {}".format(i))

def swap_letters(key):
    i, j = random.randrange(25), random.randrange(25)
    key[i], key[j] = key[j], key[i]

def swap_rows(key):
    i, j = random.randrange(5), random.randrange(5)
    for k in range(5):
        key[i * 5 + k], key[j * 5 + k] = key[j * 5 + k], key[i * 5 + k]

def swap_cols(key):
    i, j = random.randrange(5), random.randrange(5)
    for k in range(5):
        key[k * 5 + i], key[k * 5 + j] = key[k * 5 + j], key[k * 5 + i]

def rev_rows(key):
    for k in range(2):
        for j in range(5):
            key[k * 5 + j], key[(4 - k) * 5 + j] = key[(4 - k) * 5 + j], key[k * 5 + j]

def rev_cols(key):
    for k in range(2):
        for j in range(5):
            key[j * 5 + k], key[j * 5 + 4 - k] = key[j * 5 + 4 - k], key[j * 5 + k]

mutations = [swap_rows, swap_cols, list.reverse, rev_rows, rev_cols, random.shuffle]

def mutate_key(_key, MUTATE):
    key = _key.copy()
    try:
        mutations[random.randrange(MUTATE)](key)
    except IndexError:
        swap_letters(key)
    return key

def pfcrack(text, best_key, TEMP, STEP, COUNT, MUTATE):
    maxscore = fitness(decipher(text, best_key))
    T = TEMP
    last_T = T
    while T >= 0:
        if last_T - T > 2:
            last_T = T
            print("temperature: {:.2f}".format(last_T))
        for _ in range(COUNT):
            test_key = mutate_key(best_key, MUTATE)
            test_score = fitness(decipher(text, test_key))
            dF = test_score - maxscore
            if dF >= 0:
                maxscore = test_score
                best_key = test_key
            elif T > 0:
                if math.exp(dF / T) > random.random():
                    maxscore = test_score
                    best_key = test_key
        T -= STEP

    return maxscore, best_key

def decipher(text, key):
    out = []
    indmap = {b: a for a, b in enumerate(key)}
    
    for a, b in chunk(text, 2, "x"):
        ai = indmap[a]
        bi = indmap[b]
        ar = ai // 5
        br = bi // 5
        ac = ai % 5
        bc = bi % 5

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
    pf_sim_anneal(args.input.read(), args.TEMP, args.STEP, args.COUNT, args.MUTATE)
