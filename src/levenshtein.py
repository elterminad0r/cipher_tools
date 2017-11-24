"""
Calculate levenshtein distance of strings. This is an edit distance that can
for example be used to suggest corrections for spelling errors.
"""

import heapq

def levenshtein(a, b):
    """
    Levenshtein distance of strings, adapted from
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """

    # trivial cases
    if a == b:
        return 0
    elif len(a) == 0:
        return len(b)
    elif len(b) == 0:
        return len(a)

    # initialise matrix, making use of the fact that the two rows have the same
    # length. As the second row is only ever accessed after it's initialised,
    # its initial value is essentially undefined.
    matrix = [[i for i in range(len(b) + 1)] for _ in range(2)]
    for i in range(len(a)):
        matrix[1][0] = i + 1
        for j in range(len(b)):
            cost = 0 if a[i] == b[j] else 1
            matrix[1][j + 1] = min(matrix[1][j] + 1,
                                   matrix[0][j + 1] + 1,
                                   matrix[0][j] + cost)
        for j in range(len(b) + 1):
            matrix[0][j] = matrix[1][j]
    return matrix[1][len(b)]

def closest_n_matches(target, candidates, n):
    """
    Find the n strings with the smallest LD from target. Makes a copy of
    candidates as it will mutate it. If n is greater than len(candidates), an
    IndexError is raised.
    """
    # new reference so original list is not mutated
    candidates = [(levenshtein(target, can), can) for can in candidates]
    heapq.heapify(candidates)
    return [heapq.heappop(candidates)[1] for _ in range(n)]
