#!/usr/bin/env python3

"""
Call primarily command-line scripts from scripts directory
"""

import subprocess
import os
import re
import shutil

from textwrap import TextWrapper

from levenshtein import closest_n_matches

from interface_framework import restrict_args, DummyCount, UIError

scripts = {"chunk": "chunk_text.py",
           "reverse": "rev_text.py",
           "cipher": "sub_shift.py",
           "uppercase": "upper_stdin.py",
           "columnar": "perm_transposition.py",
           "railfence": "railfence.py",
           "words": "split_into_words.py",
           "strip": "strip_stdin.py",
           "matrix": "transpose_mat.py",
           "printcols": "form_columns.py",
           "invert": "invert_text.py",
           "keyphrase": "find_keywords.py",
           "markcols": "mark_cols.py",
           "stagger": "stagger.py",
           "wrap": "wrap_text.py"}

com_names = ["store", "list", *scripts]

main_docstr_pat = re.compile(r'"""\s*(.*?)\s*"""', re.MULTILINE | re.DOTALL)

def read_docs(filedict):
    docs = []
    for name, filename in filedict.items():
        with open(os.path.join(os.path.dirname(__file__),
                  "scripts", filename)) as scriptfile:
            doc, *_ = main_docstr_pat.findall(scriptfile.read())
            docs.append(doc)
    return docs

docs = read_docs(scripts)

def aggregate_docs(filedict):
    longest = max(map(len, filedict))
    return "\n".join(TextWrapper(
                        initial_indent="",
                        subsequent_indent=" " * (longest + 3),
                        width=shutil.get_terminal_size()[0]
                        ).fill("{:{l}} - {}"
                            .format(name,
                                    doc.strip(),
                                    l=longest))
                                for name, doc in zip(filedict, docs))

@restrict_args(pos=DummyCount(min_=2), pkw=[])
def call_script(state, script, *args):
    """
    Call a script from scripts/ directory. Use `!call <com> -h` to get the
    specific help menu for a command. Use `!call list` for an extended list of
    scripts.
    """
    write_output = False
    if script == "store":
        write_output = True
        if len(args) < 1:
            raise UIError("needs script to store")
        script, *args = args
    elif script == "list":
        return aggregate_docs(scripts)
    if script not in scripts:
        raise UIError(" ".join("""
                        Unrecognised script {!r}. Did you mean one of: {}?  See
                        `!call list` for more.""".split())
                    .format(script, closest_n_matches(script, com_names, 3)))
    process = subprocess.Popen(["python",
                            os.path.join(os.path.dirname(__file__),
                                         "scripts", scripts[script]), *args],
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    out, err = process.communicate(input=state.source.val)
    out_lst = ["stdout:\n{}".format(out)]
    if write_output:
        state.source.val = out
        out_lst.append("written to source")
    if err:
        out_lst.append("**STDERR: {}".format(err))
    return "\n".join(out_lst)
