#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "simulated_annealing.h"

int period;

// Bifid interface to SA lib

char *bif_decipher(char *key, char *text, char *result, int len);

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("expecting one parameter, got %d\n", argc);
        exit(EXIT_FAILURE);
    }
    sscanf(argv[1], "%d", &period);
    printf("BIFID attack using period %d\n", period);
    return sim_annealing(bif_decipher);
}

// Deciphering bifid with key

char *bif_decipher(char *key, char *text, char *result, int len) {
    int i, j;
    char a, b;
    int ai,bi, // index
        ar,br, // row
        ac,bc; // column

    for (i = 0; i < len; i += period) {
        int next = period;
        if (i + period >= len) {
            next = len - i;
        }
        for (j = 0; j < next; j ++) {
            a = text[i + (j / 2)];
            b = text[i + ((period + j) / 2)];

            ai = (int)(index(key, a) - key);
            bi = (int)(index(key, b) - key);
            ar = ai / 5;
            br = bi / 5;
            ac = ai % 5;
            bc = bi % 5;
            if (j % 2 == 0) {
                result[i + j] = key[5 * ar + br];
            } else {
                result[i + j] = key[5 * ac + bc];
            }
        }
    }
    result[i] = '\0';
    return result;
}
