#!/usr/bin/env python3

"""
Hopefully a bit of a script to tie it all together. Should support various
commands and track state, to allow the user to query and edit data.
"""

################################################################################

import shlex
import sys
import re

from input_handling import read_file
from find_doubles import get_doubles
from freq_analysis import bar_chart, alpha_counter
from make_subs import make_subs, parse_subs, pretty_subs

from collections import namedtuple

CipherState = namedtuple("CipherState", "source subs")

class UIError(Exception):
    pass

def strict_single_arg(f):
    def fun(*args):
        if len(args) == 1:
            f(*args)
        else:
            raise UIError("This function wasn't expecting an argument")
    fun.__doc__ = f.__doc__
    return fun

@strict_single_arg
def show_freq(state):
    """Display frequencies"""
    cnt = alpha_counter(state.source)
    print("Here are the frequencies:\n{}\n".format(bar_chart(cnt)))

@strict_single_arg
def show_doubles(state):
    """Show repeating adjacent identical pairs"""
    print("Here are the occurring doubles:\n{}\n"
                                .format(get_doubles(state.source)))

def delete_sub(state, *args):
    """Remove letters from the subtable"""
    print("Removing the letters {} from subs")
    for k in args:
        try:
            del state.subs[k]
        except IndexError:
            print("could not find the key {}")
    show_table()

@strict_single_arg
def show_subbed(state):
    """Show the subbed source"""
    print("Here is the substituted source:\n{}\n"
            .format(make_subs(state.source, state.subs)))

@strict_single_arg
def show_source(state):
    """Show the source"""
    print("Here is the source:\n{}\n".format(state.source))

@strict_single_arg
def show_table(state):
    """Show the subtable"""
    print("Here is the current substitution table:\n{}\n"
                .format(pretty_subs(state.subs)))

@strict_single_arg
def general_info(state):
    """Show some general info (source, table, subbed source)"""
    show_freq(state)
    show_source(state)
    show_table(state)
    show_subbed(state)

@strict_single_arg
def reset_sub(state):
    """Reset (clear) the subtable"""
    print("Resetting entire substitution table")
    state.subs.clear()

@strict_single_arg
def show_help(state):
    """Show help message"""
    print(usage)

@strict_single_arg
def exit_p(state):
    """Exit the program"""
    sys.exit()

commands = [(("frequency", "freq", "f"), show_freq),
            (("doubles", "pairs", "d"), show_doubles),
            (("delete", "remove", "r"), delete_sub),
            (("print", "p"), show_subbed),
            (("source", "s"), show_source),
            (("table", "t"), show_table),
            (("general", "g"), general_info),
            (("reset", "clear", "c"), reset_sub),
            (("help", "h"), show_help),
            (("exit", "quit", "q"), exit_p)]

def format_commands(commands):
    longest = (max(1 + len("|".join(coms)) for coms, _ in commands))
    return "\n".join("!{coms:{length}} - {desc}"
                        .format(coms="|".join(coms), 
                                desc=fun.__doc__,
                                length=longest)
                      for coms, fun in commands)

usage = """\
Anything prefixed with a ! will be considered a command. Anything else will be
interpreted as a series of substitutions to make. The available commands are as
follows:
{}
A command can be given arguments, as space-separated words after the command.
""".format(format_commands(commands))

com_pat = re.compile(r"^!([a-z]+)\b(.*)$")

def parse_com(com):
    match = com_pat.match(com)
    if match:
        return match.group(1), shlex.split(match.group(2))
    else:
        return None, com

def run():
    source = read_file()
    subs = {}
    state = CipherState(source, subs)
    show_help(state)
    while True:
        try:
            com, args = parse_com(input("Enter a command/substitutions > "))
            if com:
                for coms, fun in commands:
                    if com in coms:
                        fun(state, *args)
                        break
                else:
                    print("unrecognised command {!r}. see !help for usage"
                                        .format(com))
            else:
                insubs = parse_subs(args)
                if insubs:
                    subs.update(insubs)
                else:
                    print("looks like you didn't enter anything.. see !help")
        except UIError as uie:
            print("The following error occurred: {}".format(uie))

if __name__ == "__main__":
    run()
