# documentation for `text_interface.py`.

See also [the documentation for each function](https://github.com/goedel-gang/cipher_tools/blob/master/action_doc.md)
and [the documentation for `!call`](https://github.com/goedel-gang/cipher_tools/blob/master/call_doc.md)

The first thing you are likely to encounter is the file input. If you're not a
command line user, this will work by pasting it in, entering another newline
and pressing `ctrl-c`. For example, it might look like this:

    Manual file entry: paste in the file, or type it in line by line. When you're done, hit an extra newline to be safe and then hit ctrl-c 
    HVMTVH,
    DO DN BMZVO OJ CZVM AMJH TJP. RZ YDY KDXF PK NJHZ XCVOOZM V XJPKGZ JA HJIOCN VBJ VIY E RVN HZIODJIZY OCZMZ OJJ, NJ RZ VGMZVYT CVQZ V ADGZ JI CZM. CZM IVHZ DN EJYDZ VIY NCZ RJMFN VN GDVDNJI WZORZZI OCZ WMDODNC GDWMVMT VIY OCZ WMDODNC HPNZPH, MZNZVMXCDIB GDIFN WZORZZI VMOZAVXON VIY DHKZMDVG MJHVI OZSON, NJ OCVO ODZN DI RDOC OCZ DIOZGGDBZIXZ TJP CVQZ WZZI MZXZDQDIB. IJOCDIB NPBBZNON OCVO NCZ CVN WZZI DIQJGQZY DI VITOCDIB NCVYT VIY NCZ CVN CZGKZY RDOC NZQZMVG DINPMVIXZ AMVPY XVNZN. NCZ CVN VI DIOZMZNODIB WVXFBMJPIY. NCZ YDY V KCY JI CPHVI HDBMVODJI NOPYDZN, HVDIGT HVOCZHVODXVG HJYZGGDIB, OCZI HJQZY JI OJ NOPYT FIJRGZYBZ HDBMVODJI RCDXC BJO CZM DIOJ OCZ WDWGDJKCDGZ XDMXPDO. VAOZM BMVYPVODIB NCZ NKZIO NJHZ ODHZ RDOC JIZ JA OCZ GJIYJI VPXODJI CJPNZN RJMFDIB JI KMJQZIVIXZ WZAJMZ OVFDIB CZM XPMMZIO KJNDODJI RDOC OCZ GDWMVMT. OCZMZ MZVGGT DN IJOCDIB NPNKDXDJPN DI CZM WVXFBMJPIY VIY D RVN DIXGDIZY OJ RMDOZ CZM JAA VN V GZVY, WPO RCZI D BJO TJPM HZNNVBZ D YZXDYZY D RVIOZY OJ HZZO CZM. D OMDZY OJ NZO OCVO PK JIGT OJ WZ OJGY OCVO NCZ DN JPO JA XJPIOMT AJM V RCDGZ. DI XVDMJ.
    D RDGG NZZ TJP OCZMZ.
    CVMMT

    ^CAnything prefixed with...

The reasoning for this is that a script can only read a line of input. `ctrl-c`
sends an "interrupt signal" to the script, telling it to stop, but this will
also "corrupt" the line the script is currently trying to read, so this is made
blank for safety.

This will probably have been prefixed with something like this:

    successfully initialised
    running 3.6.3 (default, Oct  8 2017, 20:13:06) 
    [GCC 5.4.0 20160609]

This is just some diagnostic information (3.6.3 is the version of Python I'm
running, and I built it on 8th October, using GCC 5.4.0). If it says something
about `readline`, this means that the library I rely on to make the inputs
nicer isn't on your machine, so you can't cycle with up and down arrows, for
example. Apart from telling you that, I'm not sure what to do about it.

The next thing the script will do is display the following help message (or a
slightly expanded version of it if I've continued development):

    Anything prefixed with a ! will be considered a command. Anything else will be
    interpreted as a series of substitutions to make. The available commands are as
    follows:
    !frequency|freq|f       - Display frequencies - (pos=[1], pkw=['width',
                              'interv', 'pat', 'info'])
    !doubles|pairs|d        - Show repeating adjacent identical pairs - (pos=[1],
                              pkw=[])
    !word|w                 - Find words matching a prototype - (pos=[2], pkw=[])
    !runs|r                 - Display frequently repeating runs - (pos=[1],
                              pkw=['length', 'width', 'maxdisplay'])
    !delete|remove|x        - Remove letters from the subtable - (pos=[any],
                              pkw=['interv'])
    !print|p                - Show the subbed source - possible displayhooks
                              0-_make_subs 1-_alt_subs 2-_under_subs - (pos=[1],
                              pkw=['alt', 'interv'])
    !original|orig|source|o - Show the source - (pos=[1], pkw=[])
    !table|t                - Show the subtable - (pos=[1], pkw=['interv'])
    !missing                - Check for unused letters - (pos=[1], pkw=['interv',
                              'check'])
    !info|stats|i           - Display common frequency statistics - (pos=[1],
                              pkw=[])
    !clear|reset|c          - Reset (clear) the subtable - (pos=[1], pkw=['interv'])
    !make|sub|m             - Update subtable with given arguments - (pos=[any],
                              pkw=['interv'])
    !caesar|z               - Generate suggestions for a caesar cipher based on a
                              substitution - (pos=[2], pkw=[])
    !help|h                 - Show help message - (pos=[1], pkw=[])
    !undo|u                 - Undo the last substitution - (pos=[1], pkw=['interv'])
    !skip|interval|interv|s - Set the current interval - (pos=[2], pkw=[])
    !history|hist|stack     - Show current command history - (pos=[1],
                              pkw=['interv'])
    !quit|exit|q            - Exit the program - (pos=[1], pkw=[])
    !call|script            - Call a script from scripts/ directory. Use `!call
                              <com> -h` to get the specific help menu for a command.
                              Use `!call list` for an extended list of scripts. -
                              (pos=[2 <= x], pkw=[])
    !update|new             - Change source text (by pasting) - (pos=[1], pkw=[])
    !tabrecta               - Generate tabula recta from current substitutions -
                              (pos=[1], pkw=['use_tabs'])
    !state|paste            - Get pasteable series of commands for easy
                              communication/"saving" - (pos=[1], pkw=[])
    !search|regex           - Search for a regex in text. Can both highlight in
                              place and produce a long-form list. Word of warning:
                              the regex is wrapped in parens. - (pos=[2],
                              pkw=['long', 'sub'])
    A command can be given arguments, as space-separated words after the command.

Note that this menu automatically formats itself to the width of your screen.
However, this is only possible if your screen is a proper terminal, which as
far as I know idle does not provide. Therefore it would be much appreciated if
you didn't use idle but cmd or whatever happens when you run it as a python
script directly.

This gives a quick, pretty terse summary of command syntax. To expand on it a
little bit:

The "default" way the script tries to interpret anything you do is as a series
of substitutions. This follows the convention of pairs of letters representing
a substitution from the first to the second (ie `Ab` means `A` becomes `b`).

You can give many at once, generally separated by whitespace. It is case
sensitive and accepts any character (not just alphabetical ones).

Technically how the parsing works is by a `sh`-like argument parser
(`shlex.split`), so if you want to use quotes you should escape them (either by
in turn quoting them or using a backslash `\\`) or substitute whitespace, you
can use `sh` syntax, eg `" ,"`. This is entirely unimportant unless you want to
substitute a special character (ie a space, quote or backlash).

Here is how you might add some substitutions:

    Enter a command/substitutions > Hm Va Mr Ty Ch Mr   

    Here is the current substitution table:
    Ch Hm Mr Ty Va
    C -> h
    H -> m
    M -> r
    T -> y
    V -> a

    Enter a command/substitutions > " ,"
    Here is the current substitution table:
    ' ,' Ch Hm Mr Ty Va
      -> ,
    C -> h
    H -> m
    M -> r
    T -> y
    V -> a

You can see that it also prints a line which in theory you should be able to
paste straight back in.

Technically, substitutions are also a *command*, which I'll get into more
later. This is only important if you're interested in polyalphabetic ciphers.
If this is the case, once you've specified the keyword length using `!s`, you
can no longer make substitutions in this way - this is because there is no way
to tell which of the subciphers you wish to target. To make a substitution in a
certain interval, use "n!m" for some valid interval n, followed by the
substitutions you wish to make. See documentation on `!m` for a little more
detail.

Now, back to commands - this program supports more actions than just
substitutions (for one you have to be able to see what the substitutions do to
the text). These actions take the form of "commands". A command will always
start with an exclamation mark `!` character.

The notation I use here and in the program help message is

    !<command>|<alt_command>|...

This means you can call the same command as either `!command` or
`!alt_command`, etc. An example of a command you might use is:

    !print

This will print the source to the screen, making substitutions. So far all of
the commands have a shorter alias, which more often than not is the first
letter of the fully qualified command. (Notable exception is
`!delete|remove|x`, which collides with `!runs` and `!doubles`).

Some commands also accept arguments. Most often you probably don't need to
bother with these, but they can be useful (the most useful one I've found is
`!r -length`). An argument has the following syntax:

    !com -arg=val

This means call the command "`com`" and give the argument of name "`arg`" the
value "`val`". An example is `!runs`. This is a tool to analyse the frequency
of adjacent "runs" of characters. However, when you call it as just "`!runs`"
(or `!r`), it default to runs of length 3. You can specify the length of the
runs to be, for example, 2 by doing the following:

    !runs -length=2

It also only displays 20 by default. If you want to see the 30 most frequent
4-length runs, you can do

    !runs -length=4 -maxdisplay=30

In the help message, you can see the possible arguments under `pkw` - for
`!runs`, this is `pkw=['length', 'width', 'maxdisplay']`. This indicates that
`!runs` will accept the arguments "`length`", "`width`", and "`maxdisplay`".
`pkw` stands for "possible keyword arguments" - that's because these are
strictly speaking "keyword arguments", as they're given by a keyword (which is
their name).

Some functions also accept anonymous arguments. Here the argument is just given
(again, `sh`-style) after the function call, eg:

    !x A B C
    !word "B\h\aV\e"

The possible number of "positional" arguments can be seen by the `pos` value in
the help message - eg

    !word|w            - Find words matching a prototype - (pos=[2], pkw=[])

Indicating that `word` accepts two arguments. What this actually means is that
you supply it a single argument... I shall consider this a feature. Namely,
this makes explicit that fact that all functions also receive an "implicit"
argument. This argument is the "state". This allows functions like `!f` to work
without you having to pass the whole source file as an argument. This is
because the source file is stored in the "state" of the program, and this *is*
passed to `!f`, but implicitly, by the text interface rather than by you.

Some functions also accept potentially infinite arguments, eg `!x`. It has the
rather self-explanatory signature:

    !delete|remove|x        - Remove letters from the subtable - (pos=[any], pkw=['interv'])

# Now with new and improved polyalphabetic support!

Some functions also support polyalphabetic mode. These functions can accept the
keyword arg `interv` (Note that intervals are numbered starting from 0):

    !f -interv=1

Or you can use the following special shorthand:

    1!f

The command `!s` can be used to set the polyalphabetic interval. In
polyalphabetic mode, multiple substitution tables must be tracked. Because of
this, you can't just enter substitutions directly anymore. They must be fed to
the `!m` command (this has been here all along, but in single mode direct entry
acts a shortcut to `!m`). The `!m` command requires an `interv` (which can be
done with the `{num}!m` syntax), and then the familiar old substitution
arguments.

This means you can tell which functions support this by looking if `'interv'`
is one of the pkw.

Note also that when you supply *no* number, it assumes you mean `0`. This means
that in monoalphabetic mode, you use exactly the same syntax as originally, but
the program preprocesses this into polyalphabetic syntax for you.

There is also a special available argument `a` (eg `a!f`). This systematically
performs the given command for *all* possible values of n.
