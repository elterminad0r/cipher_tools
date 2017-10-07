#!/usr/bin/env python3

"""
Hopefully a bit of a framework to tie it all together. Should support various
commands and track state, to allow the user to query and edit data.
"""

################################################################################

import sys
import re
import textwrap
import string

from collections import namedtuple

from input_handling import read_file
from find_doubles import get_doubles
from find_word import find_matches
from run_freq import run_chart
from freq_analysis import bar_chart, pat_counter
from make_subs import (make_subs, parse_subs, pretty_subs,
                                    _make_subs, _alt_subs, _under_subs)

sub_dishooks = [_make_subs, _alt_subs, _under_subs]

CipherState = namedtuple("CipherState",
                        ["source",
                         "subs"])

class UIError(Exception):
    pass

def restrict_args(pos=[1], pkw=[]):
    def strict_arg(f):
        def fun(*args, **kwargs):
            if len(args) in pos:
                if all(i in pkw for i in kwargs):
                    return f(*args, **kwargs)
                else:
                    raise UIError(" ".join("""\
                                This function was expecting any of the
                                following kwargs: {} but received
                                {!r}""".format(
                                pkw,
                                 next(i for i in kwargs if i not in pkw),
                                ).split()))
            else:
                raise UIError(" ".join("""\
                        This function was expecting any of the following number
                        of arguments: {}
                        but received {}""".format(pos, len(args)).split()))
        fun.__doc__ = "{} - (pos={}, pkw={})".format(f.__doc__, pos, pkw)
        fun.pkw = pkw
        fun.pos = pos
        return fun
    return strict_arg

opt_pat = re.compile(r"^-(.*?)=(.*)$")

def read_type(option, name, typ, default):
    if option is not None:
        try:
            return typ(option)
        except ValueError:
            raise UIError("{} should be of type {}, but got {}"
                                .format(name, typ, option))
    else:
        return default

@restrict_args(pkw=["width", "interval", "pat"])
def show_freq(state, width=None, interval=None, pat=None):
    """Display frequencies"""
    width = read_type(width, "width", float, 50)
    interval = read_type(interval, "interval", int, 1)
    pat = read_type(pat, "pat", str, r"[a-zA-Z]")
    result = bar_chart(state.source, width=width, interval=interval, pat=pat,
                            subt_tab=state.subs)
    return "Here are the frequencies:\n{}\n".format(result)

@restrict_args(pkw=["length", "width", "maxdisplay"])
def show_runs(state, length=None, maxdisplay=None, width=None):
    """Display frequently repeating runs"""
    length = read_type(length, "length", int, 3)
    maxdisplay = read_type(maxdisplay, "maxdisplay", int, 20)
    width = read_type(width, "width", int, 50)
    result = run_chart(state.source, length=length, maxdisplay=maxdisplay,
                        width=width, subs=state.subs)
    return "Here are the {} most frequent runs:\n{}\n".format(maxdisplay, result)

@restrict_args()
def show_doubles(state):
    """Show repeating adjacent identical pairs"""
    return ("Here are the occurring doubles:\n{}\n"
                        .format(get_doubles(state.source, subs=state.subs)))

@restrict_args([2])
def show_words(state, pattern):
    """Find words matching a prototype"""
    return ("Here are the words matching {}:\n{}\n"
                .format(pattern, find_matches(pattern)))

def delete_sub(state, *args):
    """Remove letters from the subtable - (pos=[any], pkw=[])"""
    out_t = ["Removing the letters {} from subs".format(args)]
    for k in args:
        try:
            del state.subs[k]
        except IndexError:
            out_t.append("could not find the key {}".format(k))
    return "{}\n{}".format("\n".join(out_t), show_table(state))

@restrict_args(pkw=["alt"])
def show_subbed(state, alt=None):
    """Show the subbed source"""
    alt = read_type(alt, "alt", int, False)
    result = make_subs(state.source, state.subs, generator=sub_dishooks[alt])
    return "Here is the substituted source:\n{}\n".format(result)

@restrict_args()
def show_source(state):
    """Show the source"""
    return "Here is the source:\n{}\n".format(state.source)

@restrict_args()
def show_table(state):
    """Show the subtable"""
    return ("Here is the current substitution table:\n{}\n"
                .format(pretty_subs(state.subs)))

@restrict_args()
def table_missing(state,
      check= string.ascii_letters
           + string.digits
           + string.punctuation):
    """Check for unused letters"""
    return textwrap.dedent("""\
         Referring to set
         {}
         The following printable characters are not mapped from:
         {}
         The following printable characters are not mapped to:
         {}""").format(check,
                       " ".join(repr(i)[1:-1]
                           for i in check if i not in state.subs),
                       " ".join(repr(i)[1:-1]
                           for i in check if i not in state.subs.values()))

@restrict_args()
def general_info(state):
    """Show some general info (source, table, subbed source)"""
    return "\n\n".join([
            show_freq(state),
            show_source(state),
            show_table(state),
            show_subbed(state)])

@restrict_args()
def show_stats(state):
    """Display common frequency statistics"""
    with open("data/stats") as stats:
        return stats.read()

@restrict_args()
def reset_sub(state):
    """Reset (clear) the subtable"""
    state.subs.clear()
    return "Resetting entire substitution table"
