#!/usr/bin/env python3

"""
Detecting frequently repeating runs in a source file. Useful as some pairings
or triplets of letters are well known to occur frequently in English.
"""

################################################################################

from input_handling import read_file
from make_subs import make_subs

from collections import Counter

def get_runs(source, length):
    """
    Return a genexpr of runs in a source string, using simple slicing.
    """
    return (source[i:i + length] for i in range(len(source) - length + 1))

def run_chart(source, length, maxdisplay, width, subs={}):
    """
    Generate a more visual chart of runs.
    """
    count = Counter(get_runs(source, length))
    total = sum(count.values())
    # unpack the highest frequency in the chart
    (_, most), = count.most_common(1)
    # determine various padding values
    longest_run = max(len("{!r}".format(run)) for run in count)
    longest_i = max(len("{}".format(freq)) for freq in count.values())
    # various padding referred to
    return "\n".join("run {!r:{l}} (-> {!r:{l}}) {:{il}} times ({:6.2%}) {}"
                    .format(
                        run, make_subs(run, subs), freq, freq / total,
                        "-" * int(width * freq / most),
                        # provide padding values
                        l=longest_run, il=longest_i)
                     for run, freq in count.most_common(maxdisplay))

# if called directly, show some runs
if __name__ == "__main__":
    source = read_file()
    print("The 10 most frequent 3-runs are:\n{}\n"
                .format(run_chart(source, 3, 10, 50)))
