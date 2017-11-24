# Documentation for `split_into_words.py`

This is a command-line script to perform splitting operations on dense text. It
uses a fine-tuned prefix tree for word lookups. The algorithm is entirely
greedy but this can in fact be compensated for with whitelisting - eg in
"forthe", the algorithm sees "forth e". However, by whitelisting "for\_the",
the greedy algorithm sees a longer alternative and chooses it. You might use it
like so, from a terminal prompt:

    $ cat solutions/dense/0adense.txt 
    dearestharryithasbeentoolongsincewelastworkedtogetherandmanyshipshavepassedthroughthebosphorussincebutitispossiblethatmycurrentcasemaygiveusanopportunitytoworktogetheragainisincerelyhopesothenetworkhaspickedupalotofchatterrecentlyconcerningtheshadowantiquitiesmarketandmysuperiorsareworriedthatthismightbepartofadealsupportingaterrornetworkwearenotsurewhatthetargetisbuttheamountsbeingdiscussedarebeyondanythingihaveseenbeforesosomeoneiseitherarrangingtosellaverylargestolencollectionortheyhavefoundaparticularlyunusualitemalotofthetrafficiscomingoutofegyptandlandinginturkeywhichiswhyiwasbroughtintoinvestigatehaveyouheardanythinglondonisusuallytheclearinghouseforthesethingsandsomeonetherewiththeinitialjhasbeenmentionedreadingbetweenthelinesjseemstobeconnectedwithoneofthemajorlondoninstitutionsandiwonderedifyournetworkwaspickingupthesamesignalsonthebasisofsigintanalysiscairoseemstobethebestplaceformetostartlookingletmeknowifyouareinterestedinjoiningmethereeitherwayifyouhearanythingcouldyoupassitonbestwishesmaryam
    $ cat solutions/dense/0adense.txt | python split_into_words.py 
    initialising..
    not using nltk
    final not using
    initialised (took 0.740 secs)
    dearest harry it has been too long since we last worked together and many ships have passed through the bosphorus since but it is possible that my current case may give us an opportunity to work together again i sincerely hope so the network has picked up a lot of chatter recently concerning the shadow antiquities market and my superiors are worried that this might be part of a deal supporting a terror network we are not sure what the target is but the amounts being discussed are beyond anything i have seen before so someone is either arranging to sell a very large stolen collection or they have found a particularly unusual item a lot of the traffic is coming out of egypt and landing in turkey which is why i was brought into investigate have you heard anything london is usually the clearing house for the seth ings and someone there with the initial j has been mentioned reading between the lines j seems to be connected with one of the major london institutions and i wondered if your network was picking up the same signals on the basis of sigint analysis cairo seems to be the best place for me to start looking let me know if you are interested in joining met here either way if you hear anything could you pass it on best wishes maryam 
    $ cat solutions/dense/0adense.txt | pypy split_into_words.py  
    initialising..
    not using nltk
    final not using
    initialised (took 0.477 secs)
    ...

Here I've illustrated the file being used and the result of splitting it. This
is arguably misleading - it has been fine-tuned by testing on this file. It
reads blacklists and whitelists from an auxiliary dictionary file
`extra_words`, after building a prefix tree from all words in `words`. However,
the more it's fine tuned in this way the better it gets.
