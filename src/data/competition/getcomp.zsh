#!/usr/bin/zsh
curl "https://www.cipherchallenge.org/teams/?overall=true&a_or_b=b" | elinks -force-html -dump | grep "\* 1[= ]" 
