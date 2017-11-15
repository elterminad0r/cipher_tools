"""
Strip all non-alpha characters from a text
"""

import sys
import re

def strip(plain):
    return "".join(re.findall("[a-zA-Z]", plain))

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command line script requiring stdin")
    print(strip(sys.stdin.read()))
