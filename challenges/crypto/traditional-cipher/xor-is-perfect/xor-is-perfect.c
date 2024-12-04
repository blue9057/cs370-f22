#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <fcntl.h>

#include <unistd.h>

uint64_t seed = 0;
uint8_t key[128];
uint32_t numbers[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
uint32_t secret_numbers[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
uint8_t correct_answer[128];
uint8_t flag[128];
uint8_t *c_numbers;
uint8_t *c_secret_numbers;

int
get_random_bytes(uint8_t *bytes, ssize_t n_bytes) {
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0) {
        printf("file open failed\n");
        exit(-1);
    }
    ssize_t bytes_read = 0;
    ssize_t remaining = n_bytes;
    while (bytes_read < n_bytes) {
        ssize_t ret = read(fd, &bytes[bytes_read], remaining);
        if (ret > 0) {
            remaining -= ret;
            bytes_read += ret;
        }
        else {
            return -1;
        }
    }
    return 0;
}

void
generate_a_key(void) {
    int ret = get_random_bytes(key, 40);
    if (ret != 0) {
        printf("Failed on read random\n");
        exit(-1);
    }
}

void
generate_numbers(void) {
    for (int i=0; i<10; ++i) {
        numbers[i] = rand();
        secret_numbers[i] = rand();
    }

    c_numbers = (uint8_t *)&numbers[0];
    c_secret_numbers = (uint8_t *)&secret_numbers[0];
}

void
ask_a_question(void) {
    printf("XOR Encryption is with perfect secrecy.\n");
    printf("Generating a perfectly secret key (40 bytes)...\n\n");

    generate_a_key();
    generate_numbers();

    printf("I will send the following string encrypted with my super secret key\n");
    printf("Plaintext (2 hexadecimal digits are one byte, i.e., '41' == 0x41 == 65):\n");
    for (int i=0; i<40; ++i) {
        printf("%02x", c_numbers[i]);
    }
    printf("\n");
    printf("\n");

    printf("Ciphertext of the plaintext:\n");
    for (int i=0; i<40; ++i) {
        printf("%02x", c_numbers[i] ^ key[i]);
    }
    printf("\n");
    printf("\n");

    printf("I will also send the secret numbers, encrypted:\n");
    for (int i=0; i<40; ++i) {
        printf("%02x", c_secret_numbers[i] ^ key[i]);
    }
    printf("\n");
    printf("\n");

    memset(correct_answer, 0, 128);
    for (int i=0; i<40; ++i) {
        sprintf(&correct_answer[i*2], "%02x", c_secret_numbers[i]);
    }
    //printf("%s\n", correct_answer);


    printf("Question: what is my secret number (as 80 hexadecimal digits)?\n");
    char answer[100];
    fgets(answer, 90, stdin);
    for (int i=0; i<90; ++i) {
        if (answer[i] == '\n') {
            answer[i] = '\x00';
            break;
        }
    }
    ssize_t length = strlen(answer);
    if (length != 80) {
        printf("Incorrect digit length; please give me a 80-byte hexadecimal digits..\n");
        printf("Your input, [%s] is %d bytes long.\n", answer, length);
        exit(-1);
    }


    printf("\nYour input: %s\n", answer);

    for (int i=0; i<40; ++i) {
        if (answer[i] != correct_answer[i]) {
            printf("Your answer and the correct answer differs at byte offset %d\n", i/2);
            printf("Your    answer: %s\n", answer);
            printf("Correct answer: %s\n", correct_answer);
            exit(-1);
        }
    }

    printf("\nNow you seem to have the key, and here's the encrypted flag:\n");

    FILE *fp = fopen("flag", "r");
    if (fp) {
        fgets(flag, 80, fp);
        length = strlen(flag);
        if (length == 0) {
            printf("Flag is missing, contact yeongjin!\n");
            exit(-1);
        }
        for (int i=0; i<length; ++i) {
            printf("%02x", flag[i] ^ key[i]);
        }
        printf("\n");
        fclose(fp);
    }
    else {
        printf("Please run the program at the right directory!\n");
        exit(-1);
    }

}

int
main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    if (get_random_bytes((uint8_t *) &seed, sizeof(uint64_t))) {
        printf("Failed on reading random\n");
        exit(-1);
    }
    //printf("Seed %ld\n", seed);
    srand(seed);
    ask_a_question();
    return 0;
}
