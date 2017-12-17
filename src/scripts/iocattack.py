"""
Attack the possible IOCs for polyalphabetic cipher
"""

import re
import argparse

from collections import Counter

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("-r", "--range", type=int, default=20, help="largest interval to check")
    return parser.parse_args()

def lookat_interval(plain, start, step):
    return re.findall("[A-Z]", plain.upper())[start::step]

def ioc(cnt):
    total = sum(cnt.values())
    return (sum(freq ** 2 - freq for freq in cnt.values())
         / (total ** 2 - total))

def find_interval(plain, highest):
    candidates = (sum(ioc(Counter(lookat_interval(plain, i, interval))) for i in range(interval)) / interval for interval in range(1, highest + 1))
    for interv in ("{:2} ({:.4f}): {}".format(ind, i, "\u2796" * int(i * 800)) for ind, i in enumerate(candidates, 1)):
        print(interv)

if __name__ == "__main__":
    args = get_args()
    plain = args.input.read()
    find_interval(plain, args.range)
