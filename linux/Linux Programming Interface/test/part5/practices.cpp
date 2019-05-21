#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>

#include "error_functions.h"

void practice_2() {
    int fd = open("../data/5_2.txt", O_CREAT | O_RDWR | O_APPEND);
    if (fd == -1) {
        errExit("open error");
    }
    // 虽然偏移到了文件起点, 但是还是会写入到文件末尾
    // 设置了O_APPEND后，不管偏移到哪, 都会在文件末尾写数据
    // 即lseek对O_APPEND无效, 对READ有效
    char buf[] = "1\n2\n";

    lseek(fd, 0, SEEK_SET);
    write(fd, buf, (unsigned int)strlen(buf));

    buf[1] = '\0';
    read(fd, buf, 1);
    printf("read1 = %s\n", buf);  // 1

    lseek(fd, 0, SEEK_SET);
    read(fd, buf, 1);
    printf("read2 = %s\n", buf);  // 文件起始处内容
    if (close(fd) == -1) {
        errExit("close error");
    }
}


void practice_6() {
    char* file = (char *) "../data/5_6.txt";
    // fd1和fd2共享文件句柄, 包括偏移
    int fd1 = open(file, O_CREAT | O_RDWR | O_TRUNC);
    int fd2 = dup(fd1);
    int fd3 = open(file, O_RDWR);
    if (fd1 == -1 || fd3 == -1) {
        errExit("open error");
    }
    printf("fd1=%d, fd2=%d, fd3=%d\n", fd1, fd2, fd3);
    write(fd1, "a", 1);     // a
    write(fd2, "b", 1);     // ab, fd1和fd2共享文件偏移
    lseek(fd2, 0, SEEK_SET);
    write(fd1, "c,", 1);     // cb
    write(fd3, "d", 1);      // db

    close(fd1);
    close(fd2);
    close(fd3);
}

int main() {
//    practice_2();
    practice_6();
    return 0;
}
