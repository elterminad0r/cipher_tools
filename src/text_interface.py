#!/usr/bin/env python3

"""
A textual interface between the common interface and command line. Provides a
command-system and parsing facilities for it. Currently mainly oriented at
simple substitution ciphers.
"""

################################################################################

import shlex
import sys
import re
import textwrap

from input_handling import read_file
from make_subs import parse_subs

from interface_framework import (CipherState, UIError, restrict_args,
                                 show_freq, show_doubles, delete_sub,
                                 show_subbed, show_source, show_table,
                                 general_info, reset_sub, show_runs,
                                 show_words, table_missing, show_stats,
                                 undo, show_stack, caesar)

# regex matching an option. assumes option has been shlexed
opt_pat = re.compile(r"^-(.*?)=(.*)$")

def parse_options(opts):
    """
    Parse positional and keyword arguments from a series of arguments
    """
    # accumulate positional arguments in a list
    arg_acc = []
    # accumulate kw in a dict
    opt_acc = {}
    for opt in opts:
        # if it matches the option regex, accumulate as option
        match = opt_pat.match(opt)
        if match:
            opt_acc[match.group(1)] = match.group(2)
        # otherwise, accumulate as positional
        else:
            arg_acc.append(opt)
    return opt_acc, arg_acc

# Here are a couple more utility functions interfacing with commands, but that
# are so specific to the textual interface they're better defined here. They
# follow the same docstring convention as in interface_framework

@restrict_args()
def show_help(state):
    """Show help message"""
    return usage

@restrict_args()
def exit_p(state):
    """Exit the program"""
    sys.exit()

@restrict_args(pos=[2])
def update_table(state, new):
    out_t = []
    for k, v in new.items():
        if k in state.subs:
            out_t.append(
                "warning - the value of {} is being changed to {} (it was {})"
                                .format(k, v, state.subs[k]))
        if k not in state.source:
            out_t.append(
                "warning - the letter {} does not appear anywhere in the source text"
                                .format(k))
        state.subs[k] = v
    state.substack.append(state.subs.copy())
    return "\n".join(out_t)

# The list of commands, their aliases, and their resulting functions.
commands = [(("frequency", "freq", "f"), show_freq),
            (("doubles", "pairs", "d"), show_doubles),
            (("word", "w"), show_words),
            (("runs", "r"), show_runs),
            (("delete", "remove", "x"), delete_sub),
            (("print", "p"), show_subbed),
            (("source", "s"), show_source),
            (("table", "t"), show_table),
            (("missing", "m"), table_missing),
            (("general", "g"), general_info),
            (("info", "stats", "i"), show_stats),
            (("clear", "reset", "c"), reset_sub),
            (("caesar", "z"), caesar),
            (("help", "h"), show_help),
            (("undo", "u"), undo),
            (("history", "stack"), show_stack),
            (("quit", "exit", "q"), exit_p)]

def format_commands(commands):
    """
    Pretty command formatting, padding all the left hand sides to the same
    length, and drawing from their docstring as a short description.
    """
    longest = (max(len("|".join(coms)) for coms, _ in commands))
    return "\n".join("!{coms:{length}} - {desc}"
                        .format(coms="|".join(coms), 
                                desc=fun.__doc__,
                                length=longest)
                      for coms, fun in commands)

# general usage string
usage = """\
Anything prefixed with a ! will be considered a command. Anything else will be
interpreted as a series of substitutions to make. The available commands are as
follows:
{}
A command can be given arguments, as space-separated words after the command.
""".format(format_commands(commands))

# pattern that matches a command (anything starting in an exclamation mark
# followed by letters and a word boundary
com_pat = re.compile(r"^([0-9]*)!([a-z]+)\b(.*)$")

def parse_com(com):
    """
    Parse a command from a string. Returns the command name and parsed options
    if it's parsed as a command, otherwise return None and the original string.
    """
    match = com_pat.match(com)
    if match:
        try:
            print("targeting group {}".format(match.group(1)))
            return match.group(2), parse_options(shlex.split(match.group(3)))
        except ValueError as ve:
            raise UIError(ve)
    else:
        return None, com

def run():
    """
    Execute the user interface. Consists of mainly boilerplate
    """
    # assert stdin is a tty for interactive use
    if not sys.stdin.isatty():
        sys.exit("sys.stdin must be a tty as this is an interactive script")
    # initialise the state
    state = CipherState(source=read_file(),
                        subs={},
                        intersperse=1,
                        substack=[{}])
    print(show_help(state))
    while True:
        try:
            # parse command
            com, pargs = parse_com(input("Enter a command/substitutions > "))
            # if it's a command
            if com:
                # look for the corresponding action
                for coms, fun in commands:
                    if com in coms:
                        # execute
                        kwargs, args = pargs
                        print(fun(state, *args, **kwargs))
                        break
                # if the ccommand is unrecognised
                else:
                    raise UIError((
                        "unrecognised command {!r}. see !help, "
                        "action_doc.md or text_interface_doc.md for usage")
                            .format(com))
            # if it's to be treated as substitutions
            else:
                try:
                    insubs = parse_subs(pargs)
                except ValueError as ve:
                    raise UIError(ve)
                print(update_table(state, insubs))
                print(show_table(state))

        # friendly interfacing for a UIError
        except UIError as uie:
            print("The following error occurred: {}".format(uie))
        # dump stack trace in the case of a critical error
        except Exception as e: 
            print("\nThe following critical error occurred: {}".format(e))
            print("Full traceback:")
            raise UIError from e

# if called directly, run
if __name__ == "__main__":
    run()
