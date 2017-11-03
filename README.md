# cipher\_tools
A collection of programs to aid in cipher-cracking/cryptanalysis. If you use this and you're not a GW appreciator you're a disappointment and need to re-evaluate your life (beware as `eval` is unsafe). Currently features, among other things:

 - Pretty fully fledged textual interface, with exception handling and a functional model for commands/functions
 - Frequency analysis (including IOC calculation)
 - Substitution
 - Some facilities for polyalphabetic analysis
 - Analysis of frequently occurring runs of letters
 - Hints for unsubstituted letters
 - Display of expected frequency analysis
 - Substitution table histories
 - Utility to split an unpunctuated text into words, featuring blacklisting, whitelisting and space hinting

These are, as it stands, text-based interfaces. Hopefully it should be possible to paste in input. They rely on an installation of Python 3 (I recommend 3.6). They might be runnable by clicking the script from a file explorer?

Notice: sometimes I find catastrophic bugs, fix them and don't tell anyone. This is absolutely my fault and I'll try to stop doing this but in the meantime please make sure your version is up to date.

You can obtain the scripts by downloading them, pasting them in, or even cloning them if you're feeling really enthusiastic. (NB the scripts are all in the `src` directory.)

Here is a quick guide to installation and execution:

 - Install Python 3.6 and, by extension, Idle from https://www.python.org/downloads/. This should be pretty well documented across the web.
 - Download this repository (click Clone or download, and then "Download ZIP"). You will probably need to unzip it. Don't make any changes to the files.
 - Navigate to `src/` in the repository in the file explorer of your choice
 - Click/double click on `text_interface.py` to run it.

If you're a command line user, you can safely ignore and just clone and pull, and run `text_interface` from the CLI.

For more on how `text_interface.py` works, see [this](https://github.com/elterminad0r/cipher_tools/blob/master/text_interface_doc.md) MD file.

For documentation on each function, see [this](https://github.com/elterminad0r/cipher_tools/blob/master/action_doc.md) MD file.

For fledgling documentation on `splitting_words`, see [this](https://github.com/elterminad0r/cipher_tools/blob/master/splitting_words.md) MD file. This is probably not useful to anyone because (1) it's illegible (2) it only works from a terminal prompt.

You can also try looking at the source files in `src` - they're now pretty well documented inline. This will be more technical, terse, and may require some knowledge of Python but is guaranteed to be up to date.
