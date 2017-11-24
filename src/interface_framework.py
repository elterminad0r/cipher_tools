#!/usr/bin/env python3

"""
A framework to provide interface functions to other scripts in directory. In
theory this shouldn't be bound to any particular *user* interface, so a
separate script exists to provide textual interface to the user. If I have time
I might consider adding a GUI interface with tkinter. This program uses the
model of a "CipherState" object to represent the state of a cryptanalyst's
session. This inclused the source text, the current substitution tables, the
polyalphabetic interval and substitution histories.
"""

################################################################################

import sys
import re
import string
import shlex

from collections import namedtuple
from textwrap import dedent

from input_handling import _from_tty
from find_doubles import get_doubles
from find_word import find_matches
from run_freq import run_chart
from freq_analysis import bar_chart, pat_counter
from make_subs import (make_subs, parse_subs, pretty_subs,
                       _make_subs, _alt_subs, _under_subs)

sub_dishooks = [_make_subs, _alt_subs, _under_subs]

def set_get_width(f):
    """
    Allows calling modules to introduce a width retriever into the namespace
    """
    global get_width
    get_width = f

get_width = lambda: 80

# small class representing a state of a session. This is passed to functions
# rather than separate, specific arguments for each. This unifies call
# signatures, letting functions just look for their own stuff.
CipherState = namedtuple("CipherState",
                        ["source",
                         "subs",
                         "intersperse",
                         "substack"])

class Mutable:
    """
    Tiny dummy class that wraps a single, mutable variable. Used to store a
    mutable integer in a namedtuple.
    """
    def __init__(self, val):
        self.val = val

class DummyCount:
    """
    Dummy class to act as an infinite range (contains all integers). Could have
    used itertools.count, but membership testing on an itertools count
    apparently works by exhaustive checking, opening the line of attack of
    supplying far too many arguments
    """

    def __init__(self, min_=None, max_=None):
        self.min_ = min_
        self.max_ = max_

    def __contains__(self, x):
        if self.min_ is not None and self.max_ is not None:
            return self.min_ <= x <= self.max_
        if self.max_ is not None and self.min_ is None:
            return x <= self.max_
        if self.min_ is not None and self.max_ is None:
            return self.min_ <= x
        return True

    def __repr__(self):
        if self.min_ is not None and self.max_ is not None:
            return "[{} <= x <= {}]".format(self.min_, self.max_)
        if self.max_ is not None and self.min_ is None:
            return "[x <= {}]".format(self.max_)
        if self.min_ is not None and self.max_ is None:
            return "[{} <= x]".format(self.min_)
        return "[any]"

class UIError(Exception):
    """
    Error occurs in interfacing. Generally, ValueErrors are promoted to a
    UIError with a friendlier message, which can then be hooked to the user.
    """
    pass

def restrict_args(pos=[1], pkw=[], doc_addendum=""):
    """
    Decorator factory to perform soft (nonfatal) argument restriction. Works on
    positional and keyword arguments
    """
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
        fun.__doc__ = ("{}{} - (pos={}, pkw={})"
                    .format(dedent(f.__doc__).strip(), doc_addendum, pos, pkw))
        fun.pkw = pkw
        fun.pos = pos
        return fun
    return strict_arg

def read_type(option, name, typ, default):
    """
    General helper function to perform EAFP type conversion on arguments with
    soft failure on ValueError
    """
    if option is not None:
        try:
            return typ(option)
        except ValueError as ve:
            raise UIError("{} should be of type {}, but got {} ({})"
                                .format(name, typ, option, ve))
    else:
        return default

def pos_int(s):
    """
    Surrogate integer type that is strictly positive (greater than 0)
    """
    v = int(s)
    if not v > 0:
        raise ValueError("Was expecting a positive integer but received {}"
                            .format(v))
    return v

def int_in_range(start, stop):
    """
    Surrogate integer typefactory (thanks to first-class functions) asserting
    integer is in range. Uses the superior strict-on-end convention, as from
    Python's range() function.
    """
    def ir(s):
        v = int(s)
        if not start <= v < stop:
            raise ValueError("int {} not in range {}-{}"
                                .format(s, start, stop))
        return v
    return ir

# Here follow a series of utility functions designed to interface between a
# cipher state and the data analysis functions in other scripts. Their
# docstrings are picked up as a help message, so aren't very detailed -
# generally they aren't too complicated, just having to do lots of boilerplate
# argumenst checking and passing. These functions strictly do not print
# anything, instead returning anything they wish the user to see (printing
# would be text-interface presumptive)

@restrict_args(pkw=["width", "interv", "pat", "info"])
def show_freq(state, width=None, interv=None, pat=None, info=None):
    """
    Display frequencies
    """
    width = read_type(width, "width", float, get_width())
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    info = read_type(info, "info", int, 0)
    pat = read_type(pat, "pat", str, r"[a-zA-Z]")
    try:
        result = bar_chart(state.source.val, width=width, start=interv,
                           pat=pat, subt_tab=state.subs[interv], info=info,
                           interv=state.intersperse.val)
    except re.error:
        raise UIError("invalid regex: {!r}".format(pat))
    return "Here are the frequencies:\n{}\n".format(result)

@restrict_args(pkw=["length", "width", "maxdisplay"])
def show_runs(state, length=None, maxdisplay=None, width=None):
    """
    Display frequently repeating runs
    """
    length = read_type(length, "length", int, 3)
    maxdisplay = read_type(maxdisplay, "maxdisplay", int, 20)
    width = read_type(width, "width", float, 50)
    result = run_chart(state.source.val, length=length, maxdisplay=maxdisplay,
                        width=width)
    return "Here are the {} most frequent runs:\n{}\n".format(maxdisplay, result)

@restrict_args()
def show_doubles(state):
    """
    Show repeating adjacent identical pairs
    """
    if state.intersperse.val != 1:
        raise UIError("This function only works in single intersperse mode")
    return ("Here are the occurring doubles:\n{}\n"
                        .format(get_doubles(state.source.val, subs=state.subs[0])))

@restrict_args([2])
def show_words(state, pattern):
    """
    Find words matching a prototype
    """
    return ("Here are the words matching {}:\n{}\n"
                .format(pattern, find_matches(pattern)))

@restrict_args(pos=DummyCount(), pkw=["interv"])
def delete_sub(state, *args, interv=None):
    """
    Remove letters from the subtable
    """
    out_t = ["Removing the letters {} from subs".format(args)]
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    for k in args:
        try:
            del state.subs[interv][k]
        except KeyError:
            out_t.append("could not find the key {}".format(k))
    return "{}\n{}".format("\n".join(out_t), show_table(state, interv=interv))

@restrict_args(pkw=["alt", "interv"],
    doc_addendum=(" - possible displayhooks {}"
                        .format(" ".join("{}-{}".format(ind, i.__name__)
                                for ind, i in enumerate(sub_dishooks)))))
def show_subbed(state, alt=None):
    """
    Show the subbed source
    """
    alt = read_type(alt, "alt", int_in_range(0, len(sub_dishooks)), False)
    result = make_subs(state.source.val, state.subs, generator=sub_dishooks[alt])
    return "Here is the substituted source:\n{}\n".format(result)

@restrict_args()
def show_source(state):
    """
    Show the source
    """
    return "Here is the source:\n{}\n".format(state.source.val)

@restrict_args(pkw=["interv"])
def show_table(state, interv=None):
    """
    Show the subtable
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    return ("Here is the current substitution table:\n{}\n"
                .format(pretty_subs(state.subs[interv])))

@restrict_args(pkw=["interv", "check"])
def table_missing(state, interv=None,
      check=string.ascii_uppercase
          + string.ascii_lowercase
          + string.digits
          + string.punctuation):
    """
    Check for unused letters
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    return dedent("""\
         Referring to set
         {!r}
         The following printable characters are not mapped from:
         {!r}
         The following printable characters are not mapped to:
         {!r}""").format(check,
                       " ".join(repr(i)[1:-1]
                           for i in check if i not in state.subs[interv]),
                       " ".join(repr(i)[1:-1]
                           for i in check if i not in state.subs[interv].values()))

@restrict_args(pkw=["interv"])
def show_stack(state, interv=None):
    """
    Show current command history
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    return "\n".join(
                " ".join(shlex.quote("{}{}".format(*kv))
                        for kv in sorted(sub.items()))
                     for sub in state.substack[interv])

@restrict_args(pos=[2])
def set_interval(state, interval):
    """
    Set the current interval
    """
    interval = read_type(interval, "interval", pos_int, 1)
    state.intersperse.val = interval
    state.substack[:] = [[{}] for _ in range(interval)]
    state.subs[:] = [{} for _ in range(interval)]
    return ("successfully set interval to {},\nand reset subtables and history"
                .format(interval))

@restrict_args(pos=[2])
def caesar(state, sub):
    """
    Generate suggestions for a caesar cipher based on a substitution
    """
    if len(sub) != 2:
        raise UIError("Invalid substitution {!r}".format(sub))
    k, v = sub
    if not (k.isupper() and v.islower()):
        raise UIError("Caesar only works for upper to lower")
    k, v = map(ord, sub.lower())
    delta = v - k
    return "delta {}: {}".format(delta, 
                 " ".join(shlex.quote("{}{}".format(c.upper(),
                        chr((ord(c) + delta - ord("a")) % 26 + ord("a"))))
                     for c in string.ascii_lowercase))

@restrict_args(pkw=["interv"])
def undo(state, interv=None):
    """
    Undo the last substitution
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    if len(state.substack[interv]) > 1:
        state.substack[interv].pop()
        state.subs[interv].clear()
        state.subs[interv].update(state.substack[interv][-1])
        return show_table(state, interv=interv)
    else:
        return "Nothing to undo"

@restrict_args()
def show_stats(state):
    """
    Display common frequency statistics
    """
    with open("data/stats") as stats:
        return stats.read()

@restrict_args(pkw=["interv"])
def reset_sub(state, interv=None):
    """
    Reset (clear) the subtable
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    state.subs[interv].clear()
    return "Resetting entire substitution table in itv {}".format(interv)

# Here are a couple more utility functions interfacing with commands

@restrict_args()
def exit_p(state):
    """
    Exit the program
    """
    sys.exit()

@restrict_args(pos=DummyCount(), pkw=["interv"])
def update_table(state, *new, interv=None):
    """
    Update subtable with given arguments
    """
    interv = read_type(interv, "interv", int_in_range(0, state.intersperse.val), 0)
    out_t = []
    for kv in new:
        if len(kv) != 2:
            raise UIError("Non-pair encountered - {!r}".format(kv))
        k, v = kv
        if k in state.subs[interv]:
            out_t.append(
                "warning - the value of {} is being changed to {} (it was {})"
                                .format(k, v, state.subs[interv][k]))
        if k not in state.source.val:
            out_t.append(
                "warning - the letter {} does not appear anywhere in the source text"
                                .format(k))
        state.subs[interv][k] = v
    state.substack[interv].append(state.subs[interv].copy())
    out_t.append("made substitutions {}".format(" ".join(shlex.quote(i)
                            for i in new)))
    return "\n".join(out_t)

@restrict_args()
def update_source(state):
    """
    Change source text (by pasting)
    """
    state.source.val = _from_tty()
    return "updated source"

@restrict_args(pkw=["use_tabs"])
def format_tabula(state, use_tabs=None):
    """
    Generate tabula recta from current substitutions
    """
    use_tabs = read_type(use_tabs, "use_tabs", int, 0)
    sepchar = "\t" if use_tabs else " "
    inverse_maps = [{b.upper(): a.upper()
                        for a, b in dct.items()} for dct in state.subs]
    return "\n".join("{}:{}{}"
                    .format(ltr, sepchar, sepchar.join(dct.get(ltr, " ")
                            for dct in inverse_maps))
                                    for ltr in string.ascii_uppercase)

@restrict_args(pos=[2], pkw=["long", "sub"])
def regex_search(state, regex, long=None, sub=None):
    """
    Search for a regex in text. Can both highlight in place and produce a
    long-form list. Word of warning: the regex is wrapped in parens.
    """
    long = read_type(long, "long", int, 0)
    sub = read_type(sub, "sub", int, 1)
    plain = state.source.val
    if sub:
        plain = show_subbed(state)
    if long:
        return ("Matches of {} in text:\n{}"
                    .format(regex,
                        "\n".join(i.group(0) for i in 
                            re.finditer(regex, plain))))
    else:
        try:
            return re.sub(regex, lambda s: "**{}**".format(s.group(0)), plain)
        except ValueError:
            return "Invalid regex: {}".format(regex)
