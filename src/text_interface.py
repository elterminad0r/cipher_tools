#!/usr/bin/env python3

"""
A textual interface between the common interface and command line
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
                                 show_words, table_missing, show_stats)

from collections import namedtuple

opt_pat = re.compile(r"^-(.*?)=(.*)$")

def parse_options(opts):
    arg_acc = []
    opt_acc = {}
    for opt in opts:
        match = opt_pat.match(opt)
        if match:
            opt_acc[match.group(1)] = match.group(2)
        else:
            arg_acc.append(opt)
    return opt_acc, arg_acc

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
    return "\n".join(out_t)

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
            (("help", "h"), show_help),
            (("quit", "exit", "q"), exit_p)]

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
        try:
            return match.group(1), parse_options(shlex.split(match.group(2)))
        except ValueError as ve:
            raise UIError(ve)
    else:
        return None, com

def run():
    if not sys.stdin.isatty():
        sys.exit("sys.stdin must be a tty as this is an interactive script")
    state = CipherState(source=read_file(),
                        subs={})
    print(show_help(state))
    while True:
        try:
            com, pargs = parse_com(input("Enter a command/substitutions > "))
            if com:
                for coms, fun in commands:
                    if com in coms:
                        kwargs, args = pargs
                        print(fun(state, *args, **kwargs))
                        break
                else:
                    raise UIError((
                        "unrecognised command {!r}. see !help, "
                        "action_doc.md or text_interface_doc.md for usage")
                            .format(com))
            else:
                try:
                    insubs = parse_subs(pargs)
                except ValueError as ve:
                    raise UIError(ve)
                print(update_table(state, insubs))
                print(show_table(state))

        except UIError as uie:
            print("The following error occurred: {}".format(uie))
        except Exception as e: 
            print("\nThe following critical error occurred: {}".format(e))
            print("Full traceback:")
            raise UIError from e

if __name__ == "__main__":
    run()
