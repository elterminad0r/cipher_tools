#!/usr/bin/env python3

"""
Finding adjacently occurring pairs of letters, and performing some frequency
analysis on them. Can be especially useful knowing frequent pairing of
identical letters in english (see stats, !i)
"""

################################################################################

import re

from collections import Counter

from input_handling import read_file

# regex to match doubles, using grouping and a backreference
double_pat = re.compile(r"([A-Z])\1", re.IGNORECASE)

def get_doubles(source, subs={}):
    """
    Returns a string containing a bar-chart, frequencies and frequency ratios
    """
    return "\n".join("{!r} (-> {!r:4}) occurs {:3} times".
                     # can also show substitution - defaults to empty string
                     format(letter, subs.get(letter[0], "") * 2, frequency)
                  for letter, frequency in
                        # construct histogram
                        Counter(
                            # of each entire match
                            match.group(0)
                                for match in 
                                    double_pat.finditer(source)).
                            most_common())

# if called directly, show frequent doubles
if __name__ == "__main__":
    source = read_file()
    print("Received source:\n{}\n".format(source))
    print("Doubles in source:\n{}\n".format(get_doubles(source)))
