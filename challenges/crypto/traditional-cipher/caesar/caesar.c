#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <unistd.h>
#include <fcntl.h>

#define N_QUOTES    12
#define MAX_LEN     200

char quotes[N_QUOTES][MAX_LEN];
char transformed_quotes[N_QUOTES][MAX_LEN];
char recovered_quotes[N_QUOTES][MAX_LEN];

void init(void) {
    int flag = 0;
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd >= 0) {
        read(fd, &flag, 4);
    }
    srand(flag);
    for (int i=0; i<N_QUOTES; ++i) {
        memset(quotes[i], 0, MAX_LEN);
    }
}

void read_quotes(void) {
    FILE *fp = fopen("quotes.txt", "rt");
    if (fp != NULL) {
        for (int i=0; i<N_QUOTES; ++i) {
            fgets(quotes[i], MAX_LEN, fp);
        }
        fclose(fp);
    }
    else {
        printf("Quote loading failed! Please put the quotes.txt!\n");
    }
}

void transform_quotes(void) {
    for (int i=0; i<12; ++i) {
        size_t len = strlen(quotes[i]);
        for (int j=0; j<len; ++j) {
            if (quotes[i][j] >= 'a' && quotes[i][j] <= 'z' ||
                    quotes[i][j] >= 'A' && quotes[i][j] <= 'Z') {
                char c = quotes[i][j];
                if (c >='a') {
                    c = ((c - 'a') + 3) % 26 + 'a';
                }
                else {
                    c = ((c - 'A') + 3) % 26 + 'A';
                }
                transformed_quotes[i][j] = c;
            }
            else {
                transformed_quotes[i][j] = quotes[i][j];
            }
        }
    }
}

void un_transform_quotes(void) {
    for (int i=0; i<12; ++i) {
        size_t len = strlen(transformed_quotes[i]);
        for (int j=0; j<len; ++j) {
            if (transformed_quotes[i][j] >= 'a' && transformed_quotes[i][j] <= 'z' ||
                    transformed_quotes[i][j] >= 'A' && transformed_quotes[i][j] <= 'Z') {
                char c = transformed_quotes[i][j];
                if (c >='a') {
                    c = ((c - 'a') - 3 + 26) % 26 + 'a';
                }
                else {
                    c = ((c - 'A') - 3 + 26) % 26 + 'A';
                }
                recovered_quotes[i][j] = c;
            }
            else {
                recovered_quotes[i][j] = transformed_quotes[i][j];
            }
        }
    }
}

void test(void) {
    for (int i=0; i<12; ++i) {
        assert(strcmp(quotes[i], recovered_quotes[i]) == 0);
        /*
        printf("%s", quotes[i]);
        printf("%s", transformed_quotes[i]);
        printf("%s", recovered_quotes[i]);
        printf("\n");
        */
    }
}

void give_out_flags(void) {
    FILE *fp = fopen("flag", "r");
    if (fp) {
        char flag[200];
        memset(flag, 0, 200);
        fgets(flag, 200, fp);
        printf("%s", flag);
        fclose(fp);
    }
}

void question(void) {
    int choice = rand() % N_QUOTES;
    char plaintext[512];
    printf("Please decrypt the following ciphertext:\n");
    printf("%s", transformed_quotes[choice]);
    //printf("%s", quotes[choice]);
    printf("Give me your plaintext:\n");
    memset(plaintext, 0, 512);
    fgets(plaintext, 500, stdin);
    if (strcmp(quotes[choice], plaintext) == 0) {
        printf("Correct! Here's the flag: ");
        give_out_flags();
    }
    else {
        printf("Wrong answer!!!\n");
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    init();
    read_quotes();
    transform_quotes();
    un_transform_quotes();
    test();
    question();
}
