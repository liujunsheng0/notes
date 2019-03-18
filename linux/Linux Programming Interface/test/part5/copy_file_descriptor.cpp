#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include "error_functions.h"

int main() {
    int fd = open("../data/test.txt", O_CREAT | O_RDONLY);
    if (fd == -1) {
        errExit("open error");
    }
    int size = 100;
    int copy_fds[100];
    // dup 复制文件描述符, 指向相同的文件句柄
    for (int i = 0; i < size; i++) {
        copy_fds[i] = dup(fd);
        if (copy_fds[i] == -1) {
            errExit("dup error &d", i);
        }
        printf("fd = %d, copy_fd = %d\n", fd, copy_fds[i]);
    }
    for(int i = 0; i < size; i++) {
        if (close(copy_fds[i]) == -1) {
            printf("close %d error\n", copy_fds[i]);
        }
    }
    close(fd);
    scanf("%d", &fd);
    return 0;
}