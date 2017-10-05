A number of inputs are supported - including stdin, argv, and stdin as a tty. For all intents and purposes, if you're not working from command line, you'll be using "stdin as a tty". This means pasting/typing stuff into the script when it asks. For example, something like this might happen:

    Manual file entry: paste in the file, or type it in line by line. When you're done, hit an extra newline to be safe and then hit ctrl-c 
    a
    b
    c

Here, the script has emitted the useful-sounding text, and I've typed in "a b c", in between newlines. This is actually also a bit of a special case - when you're suppling a file, there might be a newline in the file. Hence, the script doesn't resume processing after a newline but assumes it's another line of the file. To break from the file, you press `ctrl-c`. This is the interrupt signal, which "interrupts" this process. Note that you should leave an empty line before interrupting, as the interrupt may strip away the last provided line.

Other options for suppling files are available:

    $ cat sample_in.txt | python freq_analysis.py
    $ python freq_analysis.py sample_in.txt

NB stdin should be a tty if the script wants to use any interactive input - it should warn if this goes wrong. (nothing to worry about for non CLI users)
