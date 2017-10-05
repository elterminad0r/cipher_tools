#!/usr/bin/env python3

"""
Hopefully a bit of a script to tie it all together. Should support various
commands and track state, to allow the user to query and edit data.
"""

################################################################################

from input_handling import read_file
from find_doubles import get_doubles
from freq_analysis import bar_chart, alpha_counter, line_breakdown
from make_subs import make_subs, tty_subs, pretty_subs

from collections import namedtuple

CipherState = namedtuple("CipherState", "source subs")

commands = [(("frequency", "freq", "f"), show_freq),
            (("pairs", "doubles", "p"), show_doubles),
            (("delete", "remove", "d"), delete_sub),
            (("reset", "wipe", "r"), reset_sub)
            ]

def format_commands(commands):
    return commands

usage = """\
Anything prefixed with a ! will be considered a command. Anything else will be
interpreted as a series of substitutions to make. The available commands are as
follows:
{}
A command can be given arguments, as space-separated words after the command.
""".format(format_commands(commands))

def run():
    source = read_file()
