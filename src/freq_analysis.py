#!/usr/bin/env python3

"""
Program to analyse (and possibly visualise) the frequencies of letters in text
"""

################################################################################

import re

from collections import Counter
from input_handling import read_file

alpha_pat = re.compile(r"[a-z]", re.IGNORECASE)

def alpha_counter(source):
    return Counter(alpha_pat.findall(source))

def bar_chart(cnt, w=50):
    (_, most), = cnt.most_common(1)
    total = sum(cnt.values())
    return "\n".join("{!r:4} appears {:4} times ({:6.2f}%) {}"
                          .format(letter, 
                                  frequency,
                                  frequency / total * 100,
                                  "-" * int(frequency * 50 / most))
                     for letter, frequency in cnt.most_common())

if __name__ == "__main__":
    source = read_file()
    freqs = alpha_counter(source)
    print("The given source was:\n{}\n".format(source))
    print("Frequencies are as follows:\n{}\n".format(freqs))
    print("And here's a friendlier version : D\n{}\n".format(bar_chart(freqs)))
