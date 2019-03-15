/*
 * 原子操作(atomic operation): 不可被中断的一个或一系列操作, 原子操作是许多系统得以正确执行的必要条件.
 * 所有系统调用都是以原子操作执行的,内核保证了系统调用中的所有步骤会作为独立操作,一次性执行,期间不会被其他进程或线程打断.
 *
 */

#include <sys/stat.h>
#include <fcntl.h>
#include "header.h"
#include "error_functions.h"

/*
 * 非原子操作, 多线程/进程操作同一个文件时, 无法保证顺序执行
 * 执行该main函数, 一个sleep(5), 另一个不sleep, 两个进程都会声称是自己建立的文件
 * 可使用O_CREAT | O_EXCL标志来解决上述问题
 */
int main(int argc, char *argv[]) {
    char* filename = (char *) "../data/test.txt";
    int fd;
    fd = open(filename, O_WRONLY);       /* Open 1: check if file exists */
    if (fd != -1) {                      /* Open succeeded */
        printf("[PID %ld] File \"%s\" already exists\n", (long) getpid(), filename);
        close(fd);
    } else {
        if (errno != ENOENT) {          /* Failed for unexpected reason */
            errExit("open");
        } else {
            printf("[PID %ld] File \"%s\" doesn't exist yet\n", (long) getpid(), filename);

            if (argc > 1) {             /* Delay between check and create */
                sleep(5);               /* Suspend execution for 5 seconds */
                printf("[PID %ld] Done sleeping\n", (long) getpid());
            }

            fd = open(filename, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
            if (fd == -1) {
                errExit("open");
            }
            printf("[PID %ld] Created file \"%s\" exclusively\n", (long) getpid(), filename);  /* MAY NOT BE TRUE! */
        }
    }
    return 0;
}