#!/usr/bin/env python3

"""
Detecting frequently repeating runs in a source file
"""

################################################################################

from input_handling import read_file

from collections import Counter

def get_runs(source, length):
    return (source[i:i + length] for i in range(len(source) - length + 1))

def run_chart(source, length, maxdisplay, width):
    count = Counter(get_runs(source, length))
    total = sum(count.values())
    (_, most), = count.most_common(1)
    longest_run = max(len("{!r}".format(run)) for run in count)
    longest_i = max(len("{}".format(freq)) for freq in count.values())
    return "\n".join("run {!r:{l}} {:{il}} times ({:6.2%}) {}".format(
                        run, freq, freq / total,
                        "-" * int(width * freq / most),
                        l=longest_run, il=longest_i)
                     for run, freq in count.most_common(maxdisplay))

if __name__ == "__main__":
    source = read_file()
    print("The 10 most frequent 3-runs are:\n{}\n"
                .format(run_chart(source, 3, 10, 50)))
