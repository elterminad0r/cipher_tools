#!/usr/bin/env python3

"""
Program to analyse (and possibly visualise) the frequencies of letters in text
"""

################################################################################

import re

from collections import Counter
from input_handling import read_file

fpat = re.compile(r"^\s*([a-z])\s*([0-9.]*)%.*$")

standard_freqs = []
with open("data/wiki_freq", "r") as freqfile:
    for line in freqfile:
        match = fpat.match(line)
        standard_freqs.append(match.group(1) * int(float(match.group(2)) * 1000))

def pat_counter(source, pat, interval, start):
    return Counter(re.findall(pat, source[start::interval]))

def IOC(cnt, total):
    return (sum(freq ** 2 - freq for freq in cnt.values())
         / (total ** 2 - total))

def _bar_chart(source, width, start, interval, pat, subs):
    cnt = pat_counter(source, pat, interval, start)
    longest_sub = 3
    most = 1
    longest = 4
    longest_sub = 2
    if subs:
        longest_sub = max(len("{!r}".format(i)) for i in subs.values())
    if cnt.most_common(1):
        (_, most), = cnt.most_common(1)
        longest = max(len("{!r}".format(letter)) for letter in cnt)
        longest_i = max(len("{}".format(freq)) for freq in cnt.values())
    total = sum(cnt.values())
    return "IOC: {:.5f}\n{}".format(IOC(cnt, total),
                "\n".join(
            "{!r:{l}} (-> {!r:{sl}}) appears {:{il}} times ({:6.2%}) {}"
                          .format(letter, 
                                  subs.get(letter, ""),
                                  frequency,
                                  frequency / total,
                                  "-" * int(frequency * width / most),
                                  il=longest_i,
                                  sl=longest_sub,
                                  l=longest)
                     for letter, frequency in cnt.most_common()))

def bar_chart(source, subt_tab={}, width=50, interval=1,
      pat=r"[a-zA-Z]", info=False):
    if info:
        return ("Here is the standard distribution in English:\n{}"
                .format(_bar_chart("".join(standard_freqs), width,
                            0, 1, ".", {})))

    return "\n\n".join("Interval [{}::{}]:\n{}".format(
                        i, interval,
                        _bar_chart(source, width, i, interval, pat, subt_tab))
                            for i in range(interval))

if __name__ == "__main__":
    source = read_file()
    print("The given source was:\n{}\n".format(source))
    print("Here are the frequencies:\n{}\n".format(bar_chart(source)))
