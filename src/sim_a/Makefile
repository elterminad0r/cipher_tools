.PHONY: all
all:
	make bin/bf_crack
	make bin/pf_crack
	make bin/sb_crack

bin/bf_crack: simulated_annealing.c score_text.c score_text.h quads.h bifid_attack.c
	gcc -Wall -pedantic -std=c99 -O3 bifid_attack.c score_text.c simulated_annealing.c -lm -o bin/bf_crack

bin/pf_crack: simulated_annealing.c score_text.c score_text.h quads.h playfair_attack.c
	gcc -Wall -pedantic -std=c99 -O3 playfair_attack.c score_text.c simulated_annealing.c -lm -o bin/pf_crack

bin/sb_crack: simulated_annealing.c score_text.c score_text.h quads.h subst_attack.c
	gcc -Wall -pedantic -std=c99 -O3 subst_attack.c score_text.c simulated_annealing.c -lm -o bin/sb_crack
