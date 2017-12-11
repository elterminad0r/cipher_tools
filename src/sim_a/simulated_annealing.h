typedef char *(*decipherer_type)(char *, char *, char *, int);

int sim_annealing(decipherer_type deciph);
