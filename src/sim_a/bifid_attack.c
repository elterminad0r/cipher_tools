#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "simulated_annealing.h"

#define PERIOD 4

// Bifid interface to SA lib

char *bif_decipher(char *key, char *text, char *result, int len);

int main() {
    printf("BIFID attack using period %d\n", PERIOD);
    return sim_annealing(bif_decipher);
}

// Deciphering bifid with key

char *bif_decipher(char *key, char *text, char *result, int len) {
    int i, j;
    char a, b;
    int ai,bi, // index
        ar,br, // row
        ac,bc; // column

    for (i = 0; i < len; i += PERIOD){
        int next = PERIOD;
        if (i + PERIOD >= len) {
            next = len - i;
        }
        for (j = 0; j < next; j ++){
            a = text[i + (j / 2)];
            b = text[i + ((PERIOD + j) / 2)];

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
