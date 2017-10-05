#!/usr/bin/env python3

"""
Handling input depending on presence of argv, stdin or tty idle
"""

################################################################################

import sys
import re

tty_msg = re.sub(r"\s+", " ", """\
Manual file entry: paste in the file, or type it in line by line. When you're
done, hit an extra newline to be safe and then hit ctrl-c
""")

def _from_tty():
    print(tty_msg)
    lines = []

    while True:
        try:
            lines.append(input(""))
        except KeyboardInterrupt:
            break
    return "\n".join(lines)

def read_file():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as in_file:
            return in_file.read()
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        return _from_tty()
