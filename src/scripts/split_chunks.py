import re
import sys
import string

def chunk(it, n):
    return zip(*[iter(it)] * n)

combs = {}

chstream = filter(lambda x: x != " ", iter(lambda: sys.stdin.read(1), ""))

for a in map("".join, chunk(chstream, 2)):
    if a not in combs:
        combs[a] = len(combs)
    sys.stdout.write(string.ascii_uppercase[combs[a]])
