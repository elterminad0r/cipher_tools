#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <time.h>
#include "score_text.h"

#define TEMP 20
#define STEP 0.2
#define COUNT 10000
#define MAX_STDIN 100000

// Generic "library" to optimise a decryptor-type function with simulated
// annealing. It uses a 25-size alphabet with no letter J.

typedef char *(*decipherer_type)(char *, char *, char *, int);

float annealing_run(decipherer_type deciph, char *text, int len, char* best_key);

// read ciphertext from stdin

char *read_ciphertext() {
    int i = 0;
    // allocate one extra to allow for null byte
    char *out = malloc(sizeof(char) * (MAX_STDIN + 1));
    for (char c = getchar(); c != EOF; c = getchar()) {
        if (isalpha(c)) {
            if (i > MAX_STDIN) {
                // TODO: reallocation
                printf("STDIN too big and I've not implemented dynamic allocation");
                exit(EXIT_FAILURE);
            }

            // coerce to alphabet in use
            if (toupper(c) == 'J') {
                c = 'I';
                printf("warning: converted J to I\n");
            }
            out[i++] = toupper(c);
        }
    }
    out[i] = '\0';
    return out;
}

// The "wide" SA function. Executes runs indefinitely.

int sim_annealing(decipherer_type deciph) {
    char *cipher = read_ciphertext();
    printf("ciphertext read: '%s'\n", cipher);

    int len = strlen(cipher);
    char *out = malloc(sizeof(char) * (len + 1));

    srand((unsigned)time(NULL));

    char key[] = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    double score;
    double maxscore = -99e99;

    long start = time(NULL);

    // runs until terminated
    for (int i = 1;; i++) {
        score = annealing_run(deciph, cipher, len, key);
        if(score > maxscore) {
            maxscore = score;
            printf("%lds: improvement: %.3f on it #%d\n", time(NULL) - start, score, i);
            printf("key: '%s'\n", key);
            deciph(key, cipher, out, len);
            printf("plaintext: '%s'\n", out);
        } else {
            printf("%lds: no improvement on it #%d\n", time(NULL) - start, i);
        }
    }
    return 0;
}

void swap_letters(char *key) {
    int a = rand() % 25;
    int b = rand() % 25;
    char tmp = key[a];
    key[a] = key[b];
    key[b] = tmp;
}

void swap_rows(char *key) {
    int a = rand() % 5;
    int b = rand() % 5;
    char tmp;
    for (int i = 0; i < 5; i++) {
        tmp = key[a * 5 + i];
        key[a * 5 + i] = key[b * 5 + i];
        key[b * 5 + i] = tmp;
    }
}

void swap_cols(char *key) {
    int a = rand() % 5;
    int b = rand() % 5;
    char tmp;
    for (int i = 0; i < 5; i++) {
        tmp = key[i * 5 + a];
        key[i * 5 + a] = key[i * 5 + b];
        key[i * 5 + b] = tmp;
    }
}

void shuffle(char *key) {
    char tmp;
    for (int i = 24; i >= 1; i--) {
        int j = rand() % (i + 1);
        tmp = key[j];
        key[j] = key[i];
        key[i] = tmp;
    }
} 

void mutate_key(char *new_k, char *old_k) {
    int j, k;
    int i = rand() % 50;
    switch(i) {
        case 0: strcpy(new_k, old_k); swap_rows(new_k); break;
        case 1: strcpy(new_k, old_k); swap_cols(new_k); break;       
        // reverse the whole square
        case 2:
            for(k = 0; k <25; k++)
                new_k[k] = old_k[24 - k]; new_k[25] = '\0';
            break;
        // reverse rows
        case 3:
            for(k = 0; k < 5; k++)
                for(j = 0; j < 5; j++)
                    new_k[k * 5 + j] = old_k[(4 - k) * 5 + j];
            new_k[25] = '\0';
            break;
        // reverse columns
        case 4:
            for(k = 0; k < 5; k++)
                for(j = 0; j < 5; j++)
                    new_k[j * 5 + k] = old_k[(4 - j) * 5 + k];
            new_k[25] = '\0';
            break;
        case 5: strcpy(new_k, old_k); shuffle(new_k); break;
        default:strcpy(new_k, old_k); swap_letters(new_k); break;
    }
}

// Run an "annealing", slowly decreasing temperature.

float annealing_run(decipherer_type deciph, char *text, int len, char* best_key) {
    int count;
    float T;
    char *deciphered = malloc(sizeof(char) * (len + 1));
    char conj_key[26], mx_key[26];
    double dF, maxscore, score, bestscore;
    strcpy(mx_key, best_key);
    deciph(mx_key, text, deciphered, len);
    maxscore = txt_fitness(deciphered, len);
    bestscore = maxscore;
    for (T = TEMP; T >= 0; T -= STEP) {
        printf("\rtemperature: %.3f ", T);
        fflush(stdout);
        for (count = 0; count < COUNT; count++) {
            mutate_key(conj_key, mx_key);    
            deciph(conj_key, text, deciphered, len);
            score = txt_fitness(deciphered, len);
            dF = score - maxscore;
            if (dF >= 0) {
                maxscore = score;
                strcpy(mx_key, conj_key);
            } else if(T > 0) {
                if (exp(dF / T) > 1.0 * rand() / RAND_MAX) {
                    maxscore = score;
                    strcpy(mx_key, conj_key);                
                }
            }
            if (maxscore > bestscore) {
                bestscore = maxscore;
                strcpy(best_key, mx_key);
            } 
        }
    }
    printf("\n");
    // TODO figure out what's going on here and why this causes crashes.
    //free(deciphered);
    return bestscore;
}
