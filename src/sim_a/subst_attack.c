#include <stdio.h>
#include "simulated_annealing.h"

// Substitution cipher interface to SA lib

char *subst_decipher(char *key, char *text, char *result, int len);

int main() {
    printf("SUBST attack\n");
    return sim_annealing(subst_decipher);
}

// Substitution decryption

char *subst_decipher(char *key, char *text, char *result, int len) {
    int i;
    for (i = 0; i < len; i++) {
        int idx;
        // Have to remember, no Js
        if (text[i] > 'J') {
            idx = text[i] - 'A' - 1;
        } else {
            idx = text[i] - 'A';
        }
        result[i] = key[idx];
    }
    result[i] = '\0';
    return result;
}
