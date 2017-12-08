#!/usr/bin/zsh
curl "https://www.cipherchallenge.org/teams/?overall=true&a_or_b=a" | elinks -force-html -dump | grep -E "\* [0-9]+[= ]" 
