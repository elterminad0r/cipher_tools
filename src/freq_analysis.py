#!/usr/bin/env python3

"""
Program to analyse (and possibly visualise) the frequencies of letters in text
"""

################################################################################

import re

from collections import Counter
from input_handling import read_file

def pat_counter(source, pat, interval, start):
    return Counter(re.findall(pat, source[start::interval]))

def _bar_chart(source, width, start, interval, pat):
    cnt = pat_counter(source, pat, interval, start)
    if cnt.most_common(1):
        (_, most), = cnt.most_common(1)
        longest = max(len("{!r}".format(letter)) for letter in cnt)
        longest_i = max(len("{}".format(freq)) for freq in cnt.values())
    else:
        most = 1
        longest = 4
    total = sum(cnt.values())
    return "\n".join("{!r:{l}} appears {:{il}} times ({:6.2%}) {}"
                          .format(letter, 
                                  frequency,
                                  frequency / total,
                                  "-" * int(frequency * width / most),
                                  il=longest_i,
                                  l=longest)
                     for letter, frequency in cnt.most_common())

def bar_chart(source, width=50, interval=1, pat=r"[a-zA-Z]"):
    return "\n\n".join("Interval [{}::{}]:\n{}".format(
                                i, interval,
                                _bar_chart(source, width, i, interval, pat))
                            for i in range(interval))

if __name__ == "__main__":
    source = read_file()
    print("The given source was:\n{}\n".format(source))
    print("Here are the frequencies:\n{}\n".format(bar_chart(source)))
