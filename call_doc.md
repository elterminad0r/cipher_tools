# Documentation for `!call`

`!call` is a function that serves as an interface to scripts written elsewhere.
This is useful, because some scripts just work better as command-line scripts,
but not everyone has access to/experience with the command line, so `!call`
acts as a medium between the shell and the perhaps somewhat more familiar
syntax of `text_interface`. I will not go into detail on any of the specific
functions, as these can all be obtained from the command.

This can be done by calling `!call list`. This lists the currently available
options, together with the documentation from each option. In theory, the
documentation should be formatted so that the left side of the menu is all
lined up - if this isn't happening, you should probably be using a terminal
instead of idle or something's gone wrong. Here is the current output from
`!call list` in an 80x24 terminal:

    chunk     - Splitting text into chunks (a la polybius). Use the value of the -c
                parameter to set how long blocks to accumulate are. To assign a
                letter to each block in order to allow cryptanalysis with other
                tools, use -a.
    reverse   - Reverse text. Can retain or strip punctuation, and also not reverse
                punctuation, with -s and -r respectively.
    cipher    - Script to try substitution ciphers given a keyword (useful only if
                you actually know the keyword. Currently supports caesar (-c) and
                vigenere (-v)
    uppercase - Modify the casing of text. Use -l to get lowercased text instead
    columnar  - Apply a columnar permutation transposition to a text. Takes one
                argument, which is not a keyword but a permutation. The permutation
                is formed by sotring by ascii values and assigning autoinc integers.
    railfence - Utility script to undo a rail fence cipher. Takes an optional
                argument -r which is number of rails.
    words     - Utility/convenience script to perform heuristic splitting on dense
                text. Uses a prefix tree for *very* fast lookups. Using PyPy, you
                can cut the initialisation stage from around 0.736s to 0.487s
                (around 51.13%).
    strip     - Strip all non-alpha characters from a text. This can be used eg to
                remove the spaces from blocked text.
    matrix    - Transpose a text like a matrix. Supports transposing by newlines, or
                explicitly given a block length
    printcols - Form columns from text, preserving puncutation. If you suspect
                you're dealing with a polyalphabetic cipher, you might use this to
                gain some insight. Takes one argument, which is number of columns.
    invert    - Invert the letters of text a la beaufort. Requires no parameters.
    keyphrase - Find all runs of words ("phrases") occurring in stdin with a certain
                length. (might be used to search for a keyword or name)
    markcols  - Mark polyalphabetic columns in text. This does not actually show the
                columns as columns, but provides inline markers (can be used to find
                interval to make substitutions)
    stagger   - Script that eats one line input. This is literally useless unless
                you're scripting from sh or you particularly like hitting the enter
                key
    wrap      - Wrap text, in order to make it readable. Use -w to set the width.
                This can also be used to unwrap text, by using a very large width.
                The default wrap for text_interface is the terminal window width.

The general way to call one of these scripts is `!call <name> <*args>`, where
`*args` represents an arbitrary number of arguments to pass to the script. As
these are command line scripts, you can always do `!call <script> -h` or
`--help` to get the command-line help menu. These may look a little
intimidating but provide a nice summary of the possible arguments and
functions.

Lastly, you can then store the output from a command by prepending `store` to
`call`'s arguments. For example, to make the whole of the source uppercase in
memory, use `!call store uppercase`.

Now, having seen the possible commands, we can put one of them to use. If we
were attempting challenge 3b, which has finished already, and we suspected it
was a polybius cipher, we might use it like so:

We want to firstly remove the spaces. This can be done by `strip`:

    cipher_tools 1$ !call strip
    targeting group 
    stdout:
    MLLCLDCXXMLDDDLDDCDDDLDM...

Therefore, we use `!call store strip`. Our text is now space-free. Next, we
want to chunk the text - we know there's a script to do that, but maybe we've
forgotten the exact parameters. Hence, we use `!call chunk -h`. This produces the following display:

    cipher_tools 1$ !call chunk -h
    targeting group 
    stdout:
    usage: chunk_text.py [-h] [-c CHUNK] [-a]

    Splitting text into chunks (a la polybius). Use the value of the -c parameter to set how long blocks to accumulate are. To assign a letter to each
    block in order to allow cryptanalysis with other tools, use -a.

    optional arguments:
      -h, --help            show this help message and exit
      -c CHUNK, --chunk CHUNK
                            chunk length
      -a, --accumulate      accumulate chunks into single characters


(It has become wider as this was gathered in a larger terminal)

We see that the `-c` argument takes a parameter `CHUNK`, and that `-a` takes no
parameter. Therefore, we can use `!call script -c 2 -a` to accumulate chunks of
two, and replace each of these chunks with a letter. This produces something like

    ABCDECFCGFHIEFBJFGIEFKLCIGGEFIMFBENCLJDOJF...

and now we need only use the same command with `store` attack it like a
substitution cipher.

This example might be a little contrived as there are better ways to go about
this, however some of the scripts prove mildly useful. My personal favourites
are
- `uppercase`, which transforms the whole text to uppercase so that you can
   use lowercase to denote plaintext
- `wrap`, which by default wraps the text to your screen's width. This means
  none of the words spill over edges.
- `printcols`, `markcols`, which act as column displays for polyalphabetic
  text. They are distinct as the first severely modifies the structure of the
  text.

The important thing about `!call` is that it is quite easily extensible. I will
probably let the people who need to know know if anything notable becomes
possible with `!call`.
