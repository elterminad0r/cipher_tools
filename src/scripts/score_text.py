"""
Scoring the fitness of a text by quadgram statistics
"""

import sys
import os

from hill_brute import text_as_ints

# load quadgram statistics found at
# http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-playfair/
def load_quadstats():
    with open(os.path.join(os.path.dirname(__file__),
                                          "../data/quadgramstats")) as quadstats:
        quads = [float(line) for line in quadstats]
    return quads

stats = load_quadstats()

def rolling_chunk(ls, n):
    return [ls[i:i + n] for i in range(len(ls) - n + 1)]

def fitness(text):
    """
    Assume text is a series of mod-26 integers
    """
    score = 0
    for p0, p1, p2, p3 in rolling_chunk(text, 4):
        score += stats[26 ** 3 * p0 + 26 ** 2 * p1 + 26 * p2 + p3]
    return score

if __name__ == "__main__":
    print(fitness(text_as_ints(sys.stdin.read())))
