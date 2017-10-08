#!/usr/bin/env python3

"""
Handling file input depending on presence of argv, stdin or tty idle. Mainly
present to allow script flexibility in terms of CLI testing and end-user
accessibility
"""

################################################################################

import sys

# long usage message for _from_tty
tty_msg = " ".join("""\
Manual file entry: paste in the file, or type it in line by line. When you're
done, hit an extra newline to be safe and then hit ctrl-c
""".split())

def _from_tty():
    """
    Read a file from tty stdin. As I don't want to deal with various ansi
    whatevers, especially considering the target audience is cross-platform and
    I'm not, I use input and keyboardinterrupt. It's a little hacky but seems
    to work fine.
    """
    print(tty_msg)
    lines = []

    # accumulate lines until keyboard interrupt
    while True:
        try:
            lines.append(input())
        except KeyboardInterrupt:
            break
    return "\n".join(lines)

def read_file():
    """
    Read a file from the various possible sources. Highest precedence is given
    to unlikely cases used mainly by me, ie argv and pipe stdin. Mostly stdin
    piping is unused as interactive scripts require tty stdin.
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as in_file:
            return in_file.read()
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        return _from_tty()
