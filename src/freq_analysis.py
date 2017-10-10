#!/usr/bin/env python3

"""
Program to analyse (and possibly visualise) the frequencies of letters in text.
Supports checking through different intervals, pattern matching different
subsets of the source, bar charts, index of coincidence calculation and more.
"""

################################################################################

import re

from collections import Counter
from input_handling import read_file

# pattern that matches an elinks dump of a table of letter frequencies from
# wikipedia
fpat = re.compile(r"^\s*([a-z])\s*([0-9.]*)%.*$")

# nasty hack generating an exemplary english source text to the precision of
# the bar chart
standard_freqs = []
#read from file of frequencies
with open("data/wiki_freq", "r") as freqfile:
    for line in freqfile:
        match = fpat.match(line)
        # generate a number of letters proportional to percentage
        standard_freqs.append(match.group(1) * int(float(match.group(2)) * 1000))

def pat_counter(source, pat, interval, start):
    """
    Construct a histogram of a source text given interval to check and regex to
    match characters with.
    """
    return Counter(re.findall(pat, source[start::interval]))

def IOC(cnt, total):
    """
    Calculate the index of coincidence of a given histogram. The total could be
    computed (even inline), but I know the calling function has done this
    computation so will reuse that.
    """
    if total:
        return (sum(freq ** 2 - freq for freq in cnt.values())
             / (total ** 2 - total))
    else:
        return -1

def _bar_chart(source, width, start, interval, pat, subs):
    """
    Generate a histogram from a source text, pattern and more contextual
    information. Display this as frequencies, percentages and also show
    currently implemented substitutions.
    """
    # the histogram
    cnt = pat_counter(source, pat, interval, start)
    # default values for padding
    longest_sub = 3
    most = 1
    longest = 4
    longest_sub = 2
    # try to obtain values required for padding
    if subs:
        longest_sub = max(len("{!r}".format(i)) for i in subs.values())
    if cnt.most_common(1):
        (_, most), = cnt.most_common(1)
        longest = max(len("{!r}".format(letter)) for letter in cnt)
        longest_i = max(len("{}".format(freq)) for freq in cnt.values())
    # calculate total length of observed source
    total = sum(cnt.values())
    return "IOC: {:.5f}\n{}".format(IOC(cnt, total),
                "\n".join(
            # various references to padding information
            "{!r:{l}} (-> {!r:{sl}}) appears {:{il}} times ({:6.2%}) {}"
                          .format(letter, 
                                  # default substitution information to empty
                                  # string
                                  subs.get(letter, ""),
                                  frequency,
                                  # use % formatting
                                  frequency / total,
                                  # bar on the chart
                                  "-" * int(frequency * width / most),
                                  # padding information
                                  il=longest_i,
                                  sl=longest_sub,
                                  l=longest)
                     for letter, frequency in cnt.most_common()))

def bar_chart(source, subt_tab={}, width=50, interv=1, start=0,
      pat=r"[a-zA-Z]", info=False):
    """
    Generate a series of bar charts based on just an interval. Can also show
    expected bar chart for the English language.
    """
    # showing the general chart
    if info:
        return ("Here is the standard distribution in English:\n{}"
                .format(_bar_chart("".join(standard_freqs), width,
                            0, 1, ".", {})))

    # otherwise, for each start in the interval, show bar chart
    return "Interval [{}::{}]:\n{}".format(
                    start, interv,
                    _bar_chart(source, width, start, interv, pat, subt_tab))

# if called directly, do some analysis on source
if __name__ == "__main__":
    source = read_file()
    print("The given source was:\n{}\n".format(source))
    print("Here are the frequencies:\n{}\n".format(bar_chart(source)))
