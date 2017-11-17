#!/usr/bin/env python3

"""
Call primarily command-line scripts from scripts directory
"""

import subprocess
import os

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
           "keyphrase": "find_key.py"}

@restrict_args(pos=DummyCount(min_=2), pkw=[], doc_addendum=str(scripts.keys()))
def call_script(state, script, *args):
    """call a script from scripts/ directory. Options: """
    write_output = False
    if script not in scripts:
        if script == "store":
            write_output = True
            if len(args) < 1:
                raise UIError("needs script to store")
            script, *args = args
        else:
            raise UIError("Unrecognised script {!r} - try one of {}"
                                .format(script, scripts.keys()))
    process = subprocess.Popen(["python",
                            os.path.join(os.path.dirname(__file__),
                                         "scripts", scripts[script]),
                            *args],
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
