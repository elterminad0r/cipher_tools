# Specific action documentation

All examples in this page use my custom encrypted source text [`zop13.txt`](#source). ([alternatively, source file](https://github.com/elterminad0r/cipher_tools/blob/master/src/data/zop13.txt)). This is not a part of any challenge. Try cracking it (the clue's in the name)!

# Table of contents

 - [frequency](#frequency)
 - [doubles](#doubles)
 - [word](#word)
 - [runs](#runs)
 - [delete](#delete)
 - [print](#print)
 - [source](#source)
 - [table](#table)
 - [missing](#missing)
 - [general](#general)
 - [info](#info)
 - [clear](#clear)
 - [help](#help)
 - [quit](#quit)

# frequency

    !frequency|freq|f  - Display frequencies - (pos=[1], pkw=['width', 'interval', 'pat'])

This is a command that displays letter frequencies in the text. It produces direct frequencies, percentages and a bar chart.

    Enter a command/substitutions > !f
    Here are the frequencies:
    Interval [0::1]:
    'R' (-> '') appears 92 times (13.59%) --------------------------------------------------
    'G' (-> '') appears 79 times (11.67%) ------------------------------------------
    'V' (-> '') appears 53 times ( 7.83%) ----------------------------
    'N' (-> '') appears 53 times ( 7.83%) ----------------------------
    'F' (-> '') appears 46 times ( 6.79%) -------------------------
    'B' (-> '') appears 43 times ( 6.35%) -----------------------
    'A' (-> '') appears 42 times ( 6.20%) ----------------------
    'E' (-> '') appears 33 times ( 4.87%) -----------------
    'Y' (-> '') appears 33 times ( 4.87%) -----------------
    'U' (-> '') appears 31 times ( 4.58%) ----------------
    'C' (-> '') appears 22 times ( 3.25%) -----------
    'O' (-> '') appears 21 times ( 3.10%) -----------
    'H' (-> '') appears 21 times ( 3.10%) -----------
    'L' (-> '') appears 17 times ( 2.51%) ---------
    'P' (-> '') appears 17 times ( 2.51%) ---------
    'Q' (-> '') appears 17 times ( 2.51%) ---------
    'Z' (-> '') appears 16 times ( 2.36%) --------
    'S' (-> '') appears 12 times ( 1.77%) ------
    'T' (-> '') appears 11 times ( 1.62%) -----
    'K' (-> '') appears  6 times ( 0.89%) ---
    'I' (-> '') appears  5 times ( 0.74%) --
    'J' (-> '') appears  4 times ( 0.59%) --
    'X' (-> '') appears  2 times ( 0.30%) -
    'M' (-> '') appears  1 times ( 0.15%) 

It also has a lot of arrows pointing to two single quotes around an empty void. When you've entered substitutions, these will display what substitutions are currently implemented for each letter, eg with table

    An Bo Fs Gt Mz Re Uh Yl
    A -> n
    B -> o
    F -> s
    G -> t
    M -> z
    R -> e
    U -> h
    Y -> l

this will be produced:

    Enter a command/substitutions > !f
    Here are the frequencies:
    Interval [0::1]:
    'R' (-> 'e') appears 92 times (13.59%) --------------------------------------------------
    'G' (-> 't') appears 79 times (11.67%) ------------------------------------------
    'V' (-> '' ) appears 53 times ( 7.83%) ----------------------------
    'N' (-> '' ) appears 53 times ( 7.83%) ----------------------------
    'F' (-> 's') appears 46 times ( 6.79%) -------------------------
    'B' (-> 'o') appears 43 times ( 6.35%) -----------------------
    'A' (-> 'n') appears 42 times ( 6.20%) ----------------------
    'E' (-> '' ) appears 33 times ( 4.87%) -----------------
    'Y' (-> 'l') appears 33 times ( 4.87%) -----------------
    'U' (-> 'h') appears 31 times ( 4.58%) ----------------
    'C' (-> '' ) appears 22 times ( 3.25%) -----------
    'O' (-> '' ) appears 21 times ( 3.10%) -----------
    'H' (-> '' ) appears 21 times ( 3.10%) -----------
    'L' (-> '' ) appears 17 times ( 2.51%) ---------
    'P' (-> '' ) appears 17 times ( 2.51%) ---------
    'Q' (-> '' ) appears 17 times ( 2.51%) ---------
    'Z' (-> '' ) appears 16 times ( 2.36%) --------
    'S' (-> '' ) appears 12 times ( 1.77%) ------
    'T' (-> '' ) appears 11 times ( 1.62%) -----
    'K' (-> '' ) appears  6 times ( 0.89%) ---
    'I' (-> '' ) appears  5 times ( 0.74%) --
    'J' (-> '' ) appears  4 times ( 0.59%) --
    'X' (-> '' ) appears  2 times ( 0.30%) -
    'M' (-> 'z') appears  1 times ( 0.15%) 

This function also accepts a couple of arguments:

name | function
--- | ---
`width` | Sets the maximum width of the bar chart
`interval` | Sets the "interval" to check. This is in case someone has interleaved two or more substitution ciphers - the letter distribution across the whole text may not make any sense, but across every second letter it might.
`pat` | The regex to filter the text by. By default, it uses the regex `[a-zA-Z]`, ie performs analysis on letters only. To analyse everything, use `-pat=.`. I'm sure the regex fans among you will think of many great things you can achieve with this.

# doubles

    !doubles|pairs|d   - Show repeating adjacent identical pairs - (pos=[1], pkw=[])

Finds the frequencies of adjacent letter pairings, eg:

    Enter a command/substitutions > !d
    Here are the occurring doubles:
    'GG' (-> ''  ) occurs   8 times
    'FF' (-> ''  ) occurs   4 times
    'EE' (-> ''  ) occurs   1 times
    'BB' (-> ''  ) occurs   1 times

It will also substitute in currently set substitutions, eg with table:

    Here is the current substitution table:
    Gt
    G -> t

the result becomes:

    Enter a command/substitutions > !d
    Here are the occurring doubles:
    'GG' (-> 'tt') occurs   8 times
    'FF' (-> ''  ) occurs   4 times
    'EE' (-> ''  ) occurs   1 times
    'BB' (-> ''  ) occurs   1 times

# word

    !word|w            - Find words matching a prototype - (pos=[2], pkw=[])

Greps through a dictionary of words to find words matching a given "prototype". The prototype spec is designed so that you can just paste in a word from the source, eg "GRZCGNGVBA". This will be interpreted as that all letters in the same location as a `G` must be the same, all letters in the same location as an `R`, etc. The characters used are in this case arbitrary - they could just as well be `1`, `2`.. etc. The last feature the has is that you can specify an "absolute" letter. This is when you know (or suspect) what a letter could be (for example by frequency analysis). To do this, you should pass in a string where this letter is escaped by a backslash. Because of the nature of `sh`-argument syntax, you then also have to escape it with quotes, otherwise `shlex` will eat the backslash. Here are two examples:

    Enter a command/substitutions > !w GRZCGNGVBA
    Here are the words matching GRZCGNGVBA:
    elopements
    inquisitor
    italicized
    italicizes
    orthogonal
    oxymoron's
    riverfront
    temptation
    unctuously

    Enter a command/substitutions > !w "G\eZCGNGVBA"
    Here are the words matching G\eZCGNGVBA:
    temptation

We can see that specification of the string greatly reduces the search space (although it was already pretty small). Generally `!word` is a good idea to try if you're working on a substitution cipher and see either a word where you know many of the letters, or a long word with a couple of repeated letters.

This function accepts a single argument, which is the word prototype.

# runs

    !runs|r            - Display frequently repeating runs - (pos=[1], pkw=['length', 'width', 'maxdisplay'])

This function does frequency analysis on occurring "runs" of characters in the source text. This can be useful as we might know that certain pairings occur more often in English (see [`!info`](#info)). The simple usage example is:

    Enter a command/substitutions > !r
    Here are the 20 most frequent runs:
    run ' GU'  (-> ' GU' ) 15 times ( 1.75%) --------------------------------------------------
    run ' OR'  (-> ' OR' ) 12 times ( 1.40%) ----------------------------------------
    run ' VF'  (-> ' VF' ) 10 times ( 1.17%) ---------------------------------
    run 'VF '  (-> 'VF ' ) 10 times ( 1.17%) ---------------------------------
    run 'RE '  (-> 'RE ' ) 10 times ( 1.17%) ---------------------------------
    run 'GRE'  (-> 'GRE' )  9 times ( 1.05%) ------------------------------
    run 'GUN'  (-> 'GUN' )  9 times ( 1.05%) ------------------------------
    run 'ORG'  (-> 'ORG' )  8 times ( 0.94%) --------------------------
    run 'RGG'  (-> 'RGG' )  8 times ( 0.94%) --------------------------
    run 'GGR'  (-> 'GGR' )  8 times ( 0.94%) --------------------------
    run 'E G'  (-> 'E G' )  8 times ( 0.94%) --------------------------
    run 'UNA'  (-> 'UNA' )  8 times ( 0.94%) --------------------------
    run 'NA '  (-> 'NA ' )  8 times ( 0.94%) --------------------------
    run 'GUR'  (-> 'GUR' )  7 times ( 0.82%) -----------------------
    run 'F O'  (-> 'F O' )  7 times ( 0.82%) -----------------------
    run 'ZCY'  (-> 'ZCY' )  7 times ( 0.82%) -----------------------
    run 'UR '  (-> 'UR ' )  6 times ( 0.70%) --------------------
    run 'GUB'  (-> 'GUB' )  5 times ( 0.58%) ----------------
    run 'CYR'  (-> 'CYR' )  5 times ( 0.58%) ----------------
    run ' GB'  (-> ' GB' )  5 times ( 0.58%) ----------------

It has similar substitution functionality to [`!doubles`](#doubles), and plots a very similar bar chart to [`!frequency`](#frequency).

It accepts the following parameters:

name | function
--- | ---
`width` | Sets the maximum width of the bar chart
`length` | Set the length of runs to search for
`maxdisplay` | Set how many of the most frequent runs to display


# delete

    !delete|remove|x   - Remove letters from the subtable - (pos=[any], pkw=[])

Removes chosen substitutions from the table. Supply substitutions as whitespace-separated characters. For example, starting with

    Here is the current substitution table:
    An Bo Gt Mz Re Sf Uh
    A -> n
    B -> o
    G -> t
    M -> z
    R -> e
    S -> f
    U -> h

You could do

    Enter a command/substitutions > !x A B G
    Removing the letters ('A', 'B', 'G') from subs
    Here is the current substitution table:
    Mz Re Sf Uh
    M -> z
    R -> e
    S -> f
    U -> h

If it is passed an unrecognised key it will fail softly and try to go on.

# print

    !print|p           - Show the subbed source - (pos=[1], pkw=['alt'])

Will print the source, applying substitutions in the current substitution table. By default it makes direct substitutions:

    Enter a command/substitutions > !p
    Here is the substituted source:
    the zen of CLthon, OL tVZ CeteEF

    OeNHtVfHY VF OetteE thNn HTYL.
    eKCYVPVt VF OetteE thNn VZCYVPVt.
    FVZCYe VF OetteE thNn PoZCYeK.
    PoZCYeK VF OetteE thNn PoZCYVPNteQ.
    fYNt VF OetteE thNn neFteQ.
    FCNEFe VF OetteE thNn QenFe.
    EeNQNOVYVtL PoHntF.
    FCePVNY PNFeF NEen't FCePVNY enoHTh to OEeNX the EHYeF.
    NYthoHTh CENPtVPNYVtL OeNtF CHEVtL.
    eEEoEF FhoHYQ neIeE CNFF FVYentYL.
    HnYeFF eKCYVPVtYL FVYenPeQ.
    Vn the fNPe of NZOVTHVtL, EefHFe the teZCtNtVon to THeFF.
    theEe FhoHYQ Oe one-- NnQ CEefeENOYL onYL one --oOIVoHF JNL to Qo Vt.
    NYthoHTh thNt JNL ZNL not Oe oOIVoHF Nt fVEFt HnYeFF LoH'Ee QHtPh.
    noJ VF OetteE thNn neIeE.
    NYthoHTh neIeE VF often OetteE thNn *EVTht* noJ.
    Vf the VZCYeZentNtVon VF hNEQ to eKCYNVn, Vt'F N ONQ VQeN.
    Vf the VZCYeZentNtVon VF eNFL to eKCYNVn, Vt ZNL Oe N TooQ VQeN.
    nNZeFCNPeF NEe one honXVnT TEeNt VQeN -- Yet'F Qo ZoEe of thoFe!

However there are also some alternative displayhooks:

    Enter a command/substitutions > !p -alt=1
    Here is the substituted source:
    \t\h\e \z\e\n \o\f CL\t\h\o\n, OL \tVZ C\e\t\eEF

    O\eNH\tV\fHY VF O\e\t\t\eE \t\hN\n HTYL.
    \eKCYVPV\t VF O\e\t\t\eE \t\hN\n VZCYVPV\t.
    FVZCY\e VF O\e\t\t\eE \t\hN\n P\oZCY\eK.
    P\oZCY\eK VF O\e\t\t\eE \t\hN\n P\oZCYVPN\t\eQ.
    \fYN\t VF O\e\t\t\eE \t\hN\n \n\eF\t\eQ.
    FCNEF\e VF O\e\t\t\eE \t\hN\n Q\e\nF\e.
    E\eNQNOVYV\tL P\oH\n\tF.
    FC\ePVNY PNF\eF NE\e\n'\t FC\ePVNY \e\n\oHT\h \t\o OE\eNX \t\h\e EHY\eF.
    NY\t\h\oHT\h CENP\tVPNYV\tL O\eN\tF CHEV\tL.
    \eEE\oEF F\h\oHYQ \n\eI\eE CNFF FVY\e\n\tYL.
    H\nY\eFF \eKCYVPV\tYL FVY\e\nP\eQ.
    V\n \t\h\e \fNP\e \o\f NZOVTHV\tL, E\e\fHF\e \t\h\e \t\eZC\tN\tV\o\n \t\o TH\eFF.
    \t\h\eE\e F\h\oHYQ O\e \o\n\e-- N\nQ CE\e\f\eENOYL \o\nYL \o\n\e --\oOIV\oHF JNL \t\o Q\o V\t.
    NY\t\h\oHT\h \t\hN\t JNL ZNL \n\o\t O\e \oOIV\oHF N\t \fVEF\t H\nY\eFF L\oH'E\e QH\tP\h.
    \n\oJ VF O\e\t\t\eE \t\hN\n \n\eI\eE.
    NY\t\h\oHT\h \n\eI\eE VF \o\f\t\e\n O\e\t\t\eE \t\hN\n *EVT\h\t* \n\oJ.
    V\f \t\h\e VZCY\eZ\e\n\tN\tV\o\n VF \hNEQ \t\o \eKCYNV\n, V\t'F N ONQ VQ\eN.
    V\f \t\h\e VZCY\eZ\e\n\tN\tV\o\n VF \eNFL \t\o \eKCYNV\n, V\t ZNL O\e N T\o\oQ VQ\eN.
    \nNZ\eFCNP\eF NE\e \o\n\e \h\o\nXV\nT TE\eN\t VQ\eN -- Y\e\t'F Q\o Z\oE\e \o\f \t\h\oF\e!


    Enter a command/substitutions > !p -alt=2
    Here is the substituted source:
    the( )zen( )of( )__thon(,)( )__( )t__( )_ete__(
    )(
    )_e__t_f__( )__( )_ette_( )th_n( )____(.)(
    )e______t( )__( )_ette_( )th_n( )_______t(.)(
    )_____e( )__( )_ette_( )th_n( )_o___e_(.)(
    )_o___e_( )__( )_ette_( )th_n( )_o______te_(.)(
    )f__t( )__( )_ette_( )th_n( )ne_te_(.)(
    )_____e( )__( )_ette_( )th_n( )_en_e(.)(
    )_e_______t_( )_o_nt_(.)(
    )__e____( )___e_( )__en(')t( )__e____( )eno__h( )to( )__e__( )the( )___e_(.)(
    )__tho__h( )____t_____t_( )_e_t_( )____t_(.)(
    )e__o__( )_ho___( )ne_e_( )____( )___ent__(.)(
    )_n_e__( )e______t__( )___en_e_(.)(
    )_n( )the( )f__e( )of( )_______t_(,)( )_ef__e( )the( )te__t_t_on( )to( )__e__(.)(
    )the_e( )_ho___( )_e( )one(-)(-)( )_n_( )__efe_____( )on__( )one( )(-)(-)o___o__( )___( )to( )_o( )_t(.)(
    )__tho__h( )th_t( )___( )___( )not( )_e( )o___o__( )_t( )f___t( )_n_e__( )_o_(')_e( )__t_h(.)(
    )no_( )__( )_ette_( )th_n( )ne_e_(.)(
    )__tho__h( )ne_e_( )__( )often( )_ette_( )th_n( )(*)___ht(*)( )no_(.)(
    )_f( )the( )____e_ent_t_on( )__( )h___( )to( )e_____n(,)( )_t(')_( )_( )___( )__e_(.)(
    )_f( )the( )____e_ent_t_on( )__( )e___( )to( )e_____n(,)( )_t( )___( )_e( )_( )_oo_( )__e_(.)(
    )n__e____e_( )__e( )one( )hon__n_( )__e_t( )__e_( )(-)(-)( )_et(')_( )_o( )_o_e( )of( )tho_e(!)(
    )

Accepts one optional parameter `alt`, which should be in the inclusive range `0-2`.

# source

    !source|s          - Show the source - (pos=[1], pkw=[])

Print the source:

    Enter a command/substitutions > !s
    Here is the source:
    GUR MRA BS CLGUBA, OL GVZ CRGREF

    ORNHGVSHY VF ORGGRE GUNA HTYL.
    RKCYVPVG VF ORGGRE GUNA VZCYVPVG.
    FVZCYR VF ORGGRE GUNA PBZCYRK.
    PBZCYRK VF ORGGRE GUNA PBZCYVPNGRQ.
    SYNG VF ORGGRE GUNA ARFGRQ.
    FCNEFR VF ORGGRE GUNA QRAFR.
    ERNQNOVYVGL PBHAGF.
    FCRPVNY PNFRF NERA'G FCRPVNY RABHTU GB OERNX GUR EHYRF.
    NYGUBHTU CENPGVPNYVGL ORNGF CHEVGL.
    REEBEF FUBHYQ ARIRE CNFF FVYRAGYL.
    HAYRFF RKCYVPVGYL FVYRAPRQ.
    VA GUR SNPR BS NZOVTHVGL, ERSHFR GUR GRZCGNGVBA GB THRFF.
    GURER FUBHYQ OR BAR-- NAQ CERSRENOYL BAYL BAR --BOIVBHF JNL GB QB VG.
    NYGUBHTU GUNG JNL ZNL ABG OR BOIVBHF NG SVEFG HAYRFF LBH'ER QHGPU.
    ABJ VF ORGGRE GUNA ARIRE.
    NYGUBHTU ARIRE VF BSGRA ORGGRE GUNA *EVTUG* ABJ.
    VS GUR VZCYRZRAGNGVBA VF UNEQ GB RKCYNVA, VG'F N ONQ VQRN.
    VS GUR VZCYRZRAGNGVBA VF RNFL GB RKCYNVA, VG ZNL OR N TBBQ VQRN.
    ANZRFCNPRF NER BAR UBAXVAT TERNG VQRN -- YRG'F QB ZBER BS GUBFR!

# table

    !table|t           - Show the subtable - (pos=[1], pkw=[])

Print the current substitution table, in both paste-able format and arrow format:

    Enter a command/substitutions > !t
    Here is the current substitution table:
    An Bo Gt Mz Re Sf Uh
    A -> n
    B -> o
    G -> t
    M -> z
    R -> e
    S -> f
    U -> h

Note that this command is automatically called whenever a substitution is made (even if it's empty). Therefore, you can also view the table by just pressing enter.

# missing

    !missing|m         - Check for unused letters - (pos=[1], pkw=[])

Display currently unused characters, in both sides of the table. By default it operates on the set of all alphanumeric characters. Uppercase characters are always at the start, so if that's all you're interested in you can just look at the start.

Using

    Here is the current substitution table:
    An Bo Gt Mz Re Sf Uh
    A -> n
    B -> o
    G -> t
    M -> z
    R -> e
    S -> f
    U -> h

It will produce:

    Enter a command/substitutions > !m
    Referring to set
    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    The following printable characters are not mapped from:
    C D E F H I J K L N O P Q T V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~
    The following printable characters are not mapped to:
    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d g i j k l m p q r s u v w x y 0 1 2 3 4 5 6 7 8 9 ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~

# general

    !general|g         - Show some general info (source, table, subbed source) - (pos=[1], pkw=[])

A command I've not actually ever found myself using - consider it unstable. I'm likely to remove or change it. It just ties together [`!source`](#source), [`!table`](#table), and [`!print`](#print).

# info

    !info|stats|i      - Display common frequency statistics - (pos=[1], pkw=[])

Display a possibly useful elinks dump of some statistics:

    Enter a command/substitutions > !i
       Here are the percentages that the letters of the alphabet appear in
       English:

       A   B   C   D   E    F   G   H   I   J   K   L   M
       8.2 1.5 2.8 4.3 12.7 2.2 2.0 6.1 7.0 0.2 0.8 4.0 2.4
       N   O   P   Q   R    S   T   U   V   W   X   Y   Z
       6.7 7.5 1.9 0.1 6.0  6.3 9.1 2.8 1.0 2.4 0.2 2.0 0.1

       If we put them in order of most frequent letter, it is easy to see that
       *e* is the most common letter, followed by the letter *t*:

       E    T   A   O   I   N   S   H   R   D   L   U   C
       12.7 9.1 8.2 7.5 7.0 6.7 6.3 6.1 6.0 4.3 4.0 2.8 2.8
       M    W   F   Y   G   P   B   V   K   X   J   Q   Z
       2.4  2.4 2.2 2.0 2.0 1.9 1.5 1.0 0.8 0.2 0.2 0.1 0.1

       In addition to this, English also has a number of common letter patterns
       that we can also use to help decrypt monoalphabetic ciphers:

       Common pairs            TH, EA, OF, TO, IN, IT, IS, BE, AS, AT, SO, WE,
                               HE, BY, OR, ON, DO, IF, ME, MY, UP
       Common repeated letters SS, EE, TT, FF, LL, MM and OO
       Common triplets         THE, EST, FOR, AND, HIS, ENT or THA

# clear

    !clear|reset|c     - Reset (clear) the subtable - (pos=[1], pkw=[])

Clear the current substitution table. Works like this:

Given

    Here is the current substitution table:
    An Bo Gt Mz Re Sf Uh
    A -> n
    B -> o
    G -> t
    M -> z
    R -> e
    S -> f
    U -> h

you can do:

    Enter a command/substitutions > !c
    Resetting entire substitution table
    Enter a command/substitutions > !t
    Here is the current substitution table:

# help

    !help|h            - Show help message - (pos=[1], pkw=[])

Display a half auto generated help message, which pulls from various bits of function docstrings and decorators. Currently it's:

    Anything prefixed with a ! will be considered a command. Anything else will be
    interpreted as a series of substitutions to make. The available commands are as
    follows:
    !frequency|freq|f  - Display frequencies - (pos=[1], pkw=['width', 'interval', 'pat'])
    !doubles|pairs|d   - Show repeating adjacent identical pairs - (pos=[1], pkw=[])
    !word|w            - Find words matching a prototype - (pos=[2], pkw=[])
    !runs|r            - Display frequently repeating runs - (pos=[1], pkw=['length', 'width', 'maxdisplay'])
    !delete|remove|x   - Remove letters from the subtable - (pos=[any], pkw=[])
    !print|p           - Show the subbed source - (pos=[1], pkw=['alt'])
    !source|s          - Show the source - (pos=[1], pkw=[])
    !table|t           - Show the subtable - (pos=[1], pkw=[])
    !missing|m         - Check for unused letters - (pos=[1], pkw=[])
    !general|g         - Show some general info (source, table, subbed source) - (pos=[1], pkw=[])
    !info|stats|i      - Display common frequency statistics - (pos=[1], pkw=[])
    !clear|reset|c     - Reset (clear) the subtable - (pos=[1], pkw=[])
    !help|h            - Show help message - (pos=[1], pkw=[])
    !exit|quit|q       - Exit the program - (pos=[1], pkw=[])
    A command can be given arguments, as space-separated words after the command.

It is also always displayed at the start of the program.

# exit

    !quit|exit|q       - Exit the program - (pos=[1], pkw=[])

Exit the program (also achievable by ctrl-c, ctrl-d and all manner of other things).

    Enter a command/substitutions > !q
