#include <stdio.h>

#include "score_text.h"
#include "quads.h"

// Text fitness algorithm as described at http://practicalcryptography.com/
// using data from mentioned.

float qgram[];

// integer exponenentiation as at
// https://stackoverflow.com/questions/101439/the-most-efficient-way-to-implement-an-integer-based-power-function-powint-int
int ipow(int base, int exp) {
    int result = 1;
    while (exp)
    {
        if (exp & 1)
            result *= base;
        exp >>= 1;
        base *= base;
    }
    return result;
}

// assumes that text consists only of uppercase letters(no punctuation or spaces)
double txt_fitness(char *text, int len) {
    char a, b, c, d;
    double score = 0;
    for (int i = 0; i < len - 3; i++) {
        a = text[i] - 'A';
        b = text[i + 1] - 'A';
        c = text[i + 2] - 'A';
        d = text[i + 3] - 'A';
        score += qgram[ipow(26, 3) * a + ipow(26, 2) * b + 26 * c + d];
    }
    return score;
}
