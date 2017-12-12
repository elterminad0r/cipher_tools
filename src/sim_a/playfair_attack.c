#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "simulated_annealing.h"

// Playfair interface to SA lib

char *pf_decipher(char *key, char *text, char *result, int len);

int main() {
    printf("PLAYFAIR attack\n");
    return sim_annealing(pf_decipher);
}

// Decipher playfair

char *pf_decipher(char *key, char *text, char *result, int len) {
    int i;
    char a,b;
    int a_ind, b_ind;
    int a_row, b_row;
    int a_col, b_col;
    
    for (i = 0; i < len; i += 2) {
        a = text[i];
        b = text[i + 1];
        a_ind = (int)(strchr(key,a) - key);
        b_ind = (int)(strchr(key,b) - key);
        a_row = a_ind / 5;
        b_row = b_ind / 5;
        a_col = a_ind % 5;
        b_col = b_ind % 5;
        if (a_row == b_row) {
            if (a_col == 0) {
                result[i] = key[a_ind + 4];
                result[i + 1] = key[b_ind - 1];
            } else if (b_col == 0) {
                result[i] = key[a_ind - 1];
                result[i + 1] = key[b_ind + 4];
            } else {
                result[i] = key[a_ind - 1];
                result[i + 1] = key[b_ind - 1];
            }
        } else if (a_col == b_col) {
            if (a_row == 0) {
                result[i] = key[a_ind + 20];
                result[i + 1] = key[b_ind - 5];
            } else if (b_row == 0) {
                result[i] = key[a_ind - 5];
                result[i + 1] = key[b_ind + 20];
            } else {
                result[i] = key[a_ind - 5];
                result[i + 1] = key[b_ind - 5];
            }
        } else {
            result[i] = key[5 * a_row + b_col];
            result[i + 1] = key[5 * b_row + a_col];
        }
    }
    result[i] = '\0';
    return result;
}
