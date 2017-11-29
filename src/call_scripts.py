#!/usr/bin/env python3

"""
Call primarily command-line scripts from scripts directory
"""

import subprocess
import os
import re
import shutil
import time

from textwrap import TextWrapper

from levenshtein import closest_n_matches

from interface_framework import restrict_args, DummyCount, UIError, read_type

scripts = {"chunk": "scripts/chunk_text.py",
           "reverse": "scripts/rev_text.py",
           "cipher": "scripts/sub_shift.py",
           "uppercase": "scripts/upper_stdin.py",
           "columnar": "scripts/perm_transposition.py",
           "railfence": "scripts/railfence.py",
           "words": "scripts/split_into_words.py",
           "strip": "scripts/strip_stdin.py",
           "matrix": "scripts/transpose_mat.py",
           "printcols": "scripts/form_columns.py",
           "invert": "scripts/invert_text.py",
           "keyphrase": "scripts/find_keywords.py",
           "markcols": "scripts/mark_cols.py",
           "stagger": "scripts/stagger.py",
           "wrap": "scripts/wrap_text.py",
           "ioc": "scripts/iocattack.py",
           "attack": "scripts/attacker.py",
           "autoioc": "scripts/autoioc.py",
           "autoattack": "scripts/autoattack.py",
           "autocipher": "scripts/autoencipher.py"}

com_names = ["store", "list", *scripts]

main_docstr_pat = re.compile(r'"""\s*(.*?)\s*"""', re.MULTILINE | re.DOTALL)

def read_docs(filedict):
    docs = []
    for name, filename in filedict.items():
        with open(os.path.join(os.path.dirname(__file__),
                  filename)) as scriptfile:
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

@restrict_args(pos=DummyCount(min_=2), pkw=["interpreter"])
def call_script(state, script, *args, interpreter=None):
    """
    Call a script from scripts/ directory. Use `!call <com> -h` to get the
    specific help menu for a command. Use `!call list` for an extended list of
    scripts. Accepts an interpreter argument - this is only for use if you have
    alternative installations like the PyPy JIT.
    """
    interpreter = read_type(interpreter, "interpreter", str, "python")
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
    process = subprocess.Popen([interpreter,
                        os.path.join(os.path.dirname(__file__),
                                     scripts[script]), "-", *args],
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
    start = time.time()
    out, err = process.communicate(input=state.source.val)
    dur = time.time() - start
    out_lst = ["stdout:\n{}\ntook {:.3f}s".format(out, dur)]
    if write_output:
        state.source.val = out
        out_lst.append("written to source")
    if err:
        out_lst.append("**STDERR: {}".format(err))
    return "\n".join(out_lst)
