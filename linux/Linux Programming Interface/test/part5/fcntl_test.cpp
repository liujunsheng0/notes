#include <stdio.h>
#include <fcntl.h>  // fcntl = file control

#include "error_functions.h"


// 获取文件访问模式和状态
int main() {
    int fd = open("../data/test.txt", O_CREAT | O_RDWR);
    int flags, accessMode;
    flags = fcntl(fd, F_GETFL);
    if (flags == -1) {
        Exit("fcntl error");
    }
    if (flags & O_SYNC) {
        printf("writes are synchronized\n");
    }
    accessMode = flags & O_ACCMODE;
    if (accessMode == O_RDONLY || accessMode == O_RDWR) {
        printf("file is writable\n");
    }

    return 0;
}