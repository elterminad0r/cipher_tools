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
import shutil

try:
    import readline
except ImportError:
    print("FAILED TO IMPORT READLINE (nonfatal)")

# litmus test for python 3.6 - near counter anyways
if False:
    raise 1 from 2 # YOU SHOULD INSTALL PYTHON3.6

from collections import Counter # YOU SHOULD INSTALL PYTHON3.6
from textwrap import TextWrapper, dedent, fill

from levenshtein import closest_n_matches

from input_handling import read_file
from make_subs import parse_subs

from interface_framework import (CipherState, UIError, DummyCount,
                                 restrict_args, show_freq, show_doubles,
                                 delete_sub, show_subbed, show_source,
                                 show_table, reset_sub, show_runs, show_words,
                                 table_missing, show_stats, undo, show_stack,
                                 caesar, set_interval, exit_p, update_table,
                                 Mutable, update_source, format_tabula,
                                 set_get_width, set_get_width, regex_search)

set_get_width(lambda: shutil.get_terminal_size()[0])

try:
    from call_scripts import call_script
except SyntaxError:
    sys.exit("YOU SHOULD INSTALL PYTHON 3.6")

def verify_exit():
    """
    Verify if a user really wants to exit
    """
    try:
        do_ex = input("\nare you sure you want to exit? ").lower()
        return not do_ex or do_ex[0] == "y"
    except (KeyboardInterrupt, EOFError):
        return True

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

# commands more closely tied to the text interface - still follows the same
# conventions

@restrict_args()
def show_help(state):
    """
    Show help message
    """
    return get_usage() 

@restrict_args()
def get_pasteable(state):
    """
    Get pasteable series of commands for easy communication/"saving"
    """
    return "!s {}\n{}".format(state.intersperse.val,
                        "\n".join("{}!m {}".format(ind, 
                            " ".join(shlex.quote("{}{}".format(*kv))
                                for kv in sorted(subs.items())))
                                    for ind, subs in enumerate(state.subs)))

# The list of commands, their aliases, and their resulting functions.
commands = [(("frequency", "freq", "f"), show_freq),
            (("doubles", "pairs", "d"), show_doubles),
            (("word", "w"), show_words),
            (("runs", "r"), show_runs),
            (("delete", "remove", "x"), delete_sub),
            (("print", "p"), show_subbed),
            (("original", "orig", "source", "o"), show_source),
            (("table", "t"), show_table),
            (("missing",), table_missing),
            (("info", "stats", "i"), show_stats),
            (("clear", "reset", "c"), reset_sub),
            (("make", "sub", "m"), update_table),
            (("caesar", "z"), caesar),
            (("help", "h"), show_help),
            (("undo", "u"), undo),
            (("skip", "interval", "interv", "s"), set_interval),
            (("history", "hist", "stack"), show_stack),
            (("quit", "exit", "q"), exit_p),
            (("call", "script"), call_script),
            (("update", "new"), update_source),
            (("tabrecta",), format_tabula),
            (("state", "paste"), get_pasteable),
            (("search", "regex"), regex_search)]

com_names = [i for l in commands for i in l[0]]

# assert there are no duplicate commands
if __debug__:
    assert len(com_names) == len(set(com_names))

print("successfully initialised")

def format_commands(commands):
    """
    Pretty command formatting, padding all the left hand sides to the same
    length, and drawing from their docstring as a short description.
    """
    longest = (max(len("|".join(coms)) for coms, _ in commands))
    return "\n".join(TextWrapper(
                        initial_indent="",
                        subsequent_indent=" " * (longest + 4),
                        drop_whitespace=True,
                        width=shutil.get_terminal_size()[0]
                        ).fill("!{coms:{length}} - {desc}"
                        .format(coms="|".join(coms), 
                                desc=dedent(fun.__doc__).strip(),
                                length=longest))
                      for coms, fun in commands)

def get_usage():
    """
    Generate the "help menu"
    """
    return dedent("""\
    Anything prefixed with a ! will be considered a command. Anything else will be
    interpreted as a series of substitutions to make. The available commands are as
    follows:
    {}
    A command can be given arguments, as space-separated words after the command.
    """).format(format_commands(commands))

# pattern that matches a command (anything starting in an exclamation mark
# followed by letters and a word boundary
com_pat = re.compile(r"^([0-9]*|a)!([a-zA-Z]+)\b(.*)$")

def parse_com(com):
    """
    Parse a command from a string. Returns the command name and parsed options
    if it's parsed as a command, otherwise return None and the original string.
    """
    match = com_pat.match(com)
    if match:
        try:
            print("targeting group {}".format(match.group(1)))
            return match.group(2), parse_options(shlex.split(match.group(3))), match.group(1)
        except ValueError as ve:
            raise UIError(ve)
    else:
        return None, com, None

def run():
    """
    Execute the user interface. Consists of mainly boilerplate
    """
    # assert stdin is a tty for interactive use
    if not sys.stdin.isatty():
        sys.exit("sys.stdin must be a tty as this is an interactive script")


    # initialise the state
    state = CipherState(source=Mutable(read_file()),
                        subs=[{}],
                        intersperse=Mutable(1),
                        substack=[[{}]])
    print(show_help(state))
    while True:
        try:
            # parse command
            com, pargs, interv = parse_com(input("cipher_tools {}$ ".format(state.intersperse.val)))
            # if it's a command
            if com:
                # look for the corresponding action
                for coms, fun in commands:
                    if com in coms:
                        # execute
                        kwargs, args = pargs

                        # handling functions that operate on intervals
                        if interv == "a":
                            for it in range(state.intersperse.val):
                                print("Executing for interv={}".format(it))
                                print(fun(state, *args, interv=it, **kwargs))
                        elif interv:
                            try:
                                it = int(interv)
                            except ValueError:
                                raise UIError("Invalid interval {!r}".format(interv))
                            print(fun(state, *args, interv=it, **kwargs))

                        else:
                            print(fun(state, *args, **kwargs))

                        break
                # if the command is unrecognised
                else:
                    raise UIError(" ".join("""\
                      unrecognised command {!r}. Did you mean any of {}? see
                      !help, action_doc.md or text_interface_doc.md for usage
                      """.split())
                        .format(com,
                             closest_n_matches(com.lower(), com_names, 3)))
            # if it's to be treated as substitutions
            else:
                if state.intersperse.val != 1:
                    raise UIError("In polyalphabetic mode use !m")
                try:
                    insubs = shlex.split(pargs)
                except ValueError as ve:
                    raise UIError(ve)
                print(update_table(state, *insubs, interv=0))

        except (KeyboardInterrupt, EOFError):
            if verify_exit():
                print("bye")
                break

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
    print("running {}".format(sys.version))
    run()
