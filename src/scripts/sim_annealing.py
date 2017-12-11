"""
Attacking a playfair cipher by simulated annealing
"""

import itertools
import string
import math
import random
import time

from collections import defaultdict

from hill_brute import text_as_ints
from score_text import fitness

def sim_anneal(decryptor, text, temp, step, count, mutate, pbound):
    start = time.time()
    text = text_as_ints(text)
    key = text_as_ints(string.ascii_uppercase.replace("J", ""))
    maxscore = float("-inf")
    for i in itertools.count():
        score, conj_key = crack(decryptor, text, key, temp, step, count, mutate, pbound)
        if score > maxscore:
            maxscore = score
            key = conj_key
            print("it {} yields score {}".format(i, maxscore))
            print("took {:.3f}s".format(time.time() - start))
            print("key: {}".format(key))
            print("plaintext: {}".format("".join(string.ascii_uppercase[i] for i in decryptor(text, key))))
        else:
            print("no improvement at iteration {}".format(i))

def swap_letters(key):
    i, j = random.randrange(25), random.randrange(25)
    key[i], key[j] = key[j], key[i]

def swap_rows(key):
    i, j = random.randrange(5) * 5, random.randrange(5) * 5
    key[i:i + 5], key[j:j + 5] = key[j:j + 5], key[i:i + 5]

def swap_cols(key):
    i, j = random.randrange(5), random.randrange(5)
    key[i::5], key[j::5] = key[j::5], key[i::5]

def rev_rows(key):
    for k in range(0, 15, 5):
        key[k:k + 5], key[20 - k:25 - k] = key[20 - k: 25 - k], key[k: k + 5]

def rev_cols(key):
    for k in range(2):
        key[k::5], key[4 - k::5] = key[4 - k::5], key[k::5]

mutations = [swap_rows, swap_cols, list.reverse, rev_rows, rev_cols, random.shuffle]

for mut in mutations:
    k = list(range(25))
    mut(k)
    print(k)

def mutate_key(_key, MUTATE):
    key = _key.copy()
    try:
        mutations[random.randrange(MUTATE)](key)
    except IndexError:
        swap_letters(key)
    return key

def crack(decryptor, text, best_key, TEMP, STEP, COUNT, MUTATE, PRINT_BOUND):
    maxscore = fitness(decryptor(text, best_key))
    T = TEMP
    last_T = T
    start = time.time()
    while T >= 0:
        if last_T - T > PRINT_BOUND:
            last_T = T
            print("temperature: {:.2f} (at {:.3f}s)".format(last_T, time.time() - start))
        for _ in range(COUNT):
            test_key = mutate_key(best_key, MUTATE)
            test_score = fitness(decryptor(text, test_key))
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
