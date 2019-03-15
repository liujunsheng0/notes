#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include "error_functions.h"

int main() {
    int fd = open("../data/test.txt", O_CREAT | O_RDONLY);
    if (fd == -1) {
        errExit("open error");
    }
    // dup 复制文件描述符, 指向相同的文件句柄
    for (int i = 0; i < 1000; i++) {
        if (dup(fd) == -1) {
            errExit("dup error &d", i);
        }
    }
    close(fd);
    scanf("%d", &fd);
    return 0;
}