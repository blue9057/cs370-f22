#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <unistd.h>

uint8_t pwd_path[512];
uint8_t script_path[512];
uint8_t command[1024];

void
strip(char *p) {
    ssize_t len = strlen(p);
    if (len != 0) {
        for (ssize_t i = len-1; i>=0; --i) {
            if (p[i] == '\n' || p[i] == ' ' || p[i] == '\t') {
                p[i] = '\0';
            }
            else {
                break;
            }
        }
    }
}

int main() {
    setregid(getegid(), getegid());
    FILE *fp = fopen("/home/labs/crypto/sha-256/config", "rb");
    fgets(pwd_path, 512, fp);
    fgets(script_path, 512, fp);
    size_t pwd_len = strlen(pwd_path);
    size_t script_len = strlen(script_path);
    strip(pwd_path);
    strip(script_path);
    snprintf(command, 1024, "%s/%s", pwd_path, script_path);
    printf("Running Command: [%s]\n", command);
    system(command);
}
