#!/usr/bin/env python3

"""
Wrap text, in order to make it readable. Use -w to set the width. This can also
be used to unwrap text, by using a very large width. The default wrap for
text_interface is the terminal window width.
"""

import sys
import argparse
import shutil

from textwrap import fill

def get_paras(text):
    return text.splitlines()

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("-w", "--width", type=int,
                                help="width to wrap to")
    return parser.parse_args()

def wrap_paras(text, width):
    return "\n".join(fill(para, width) for para in get_paras(text))

if __name__ == "__main__":
    args = get_args()
    if not args.width:
        args.width = shutil.get_terminal_size()[0]
    sys.stdout.write(wrap_paras(args.input.read(), args.width))
