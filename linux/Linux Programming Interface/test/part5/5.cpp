// Linux 系统编程手册 第五章 深入探究文件I/O

#include "header.h"
#include "error_functions.h"

using namespace std;

/* 原子操作
 * 原子操作(atomic operation): 不可被中断的一个或一系列操作, 原子操作是许多系统得以正确执行的必要条件.
 * 所有系统调用都是以原子操作执行的,内核保证了系统调用中的所有步骤会作为独立操作,一次性执行,期间不会被其他进程或线程打断.
 *
 * ./a.out 0 10 &
 * ./a.out 0 0
 */
void atomic_operation(uint st) {
    // 检查文件是否存在, 如果不存在则新建文件. 多进程下会出现问题, 因为不是原子操作
    // 可使用O_CREAT | O_EXCL标志来解决上述问题
    string filename = "error.txt";
    int fd;
    long pid = (long) getpid();

    fd = open(filename.data(), O_WRONLY);
    if (fd != -1) {
        printf("[pid %ld] file %s exist\n", pid, filename.data());
        close(fd);
        return;
    }

    if (errno != ENOENT) {
        Exit("open");
    }
    printf("[pid %ld] file %s doesn't exist\n", pid, filename.data());
    sleep(st);
    printf("[pid %ld] done sleeping st=%d\n", pid, st);

    fd = open(filename.data(), O_WRONLY | O_CREAT, 0666);
    if (fd == -1) {
        Exit("open");
    }
    char s_pid[10] = "      \n";
    sprintf(s_pid, "%ld", (long) getpid());

    // 向test.txt写入pid
    write(fd, s_pid, 10);
    if (-1 == close(fd)) {
        Exit("close");
    }
    printf("[pid %ld] created file %s\n", (long) getpid(), filename.data());
}


void file_mode() {
    mode_t mode = 0666;
    int fd = open("test.txt", O_CREAT | O_RDWR | O_TRUNC, mode);
    int flag, access_mode;

    flag = fcntl(fd, F_GETFL);
    if (flag == -1) {
        Exit("fcntl error");
    }
    if (flag & O_SYNC) {
        printf("writes are synchronized\n");
    }
    access_mode = flag & O_ACCMODE;
    if (access_mode | O_RDONLY) {
        printf("file is readable\n");
    }

    if (access_mode | O_WRONLY || access_mode | O_RDWR) {
        printf("file is writable\n");
    }
}

/*
 * 多个文件描述符可指向同一打开文件, 这些文件描述符可在相同或不同的进程中打开
 *
 * 要理解文件描述符和打开文件之间的关系, 需要查看*内核*维护的三个数据结构:
 *     1. 进程级的文件描述符表
 *     2. 系统级的打开文件表
 *     3. 文件系统的i-node表
 *
 *  进程级的文件描述符表, 针对每个进程, 内核为其维护打开文件的描述符表. 记录了文件描述符相关信息
 *      1. 控制文件描述符操作的一组标志
 *      2. 对打开文件句柄的引用
 *
 *  系统级的打开文件表, 内核对所有打开的文件维护一个系统级的描述表格(打开文件表), 表中的内容为打开文件句柄(open file handle).
 *  文件句柄存储了与打开文件相关的全部信息, 如
 *      1. 当前文件偏移量
 *      2. 打开文件时使用的状态标志, 即open()的flags参数
 *      3. 文件访问模式,  即open()的flags参数中的只读, 只写, 读写模式中的一个
 *      4. 与信号驱动I/O相关的设置
 *      5. 对该文件i-node对象的引用
 *
 *  i-node表
 *      1. 文件类型和访问权限
 *      2. 一个指针, 指向该文件所持有的锁的列表
 *      3. 文件的各种属性, 包括文件大小, 修改时间等
 *
 *  由file_and_file_descriptor.png可知, 文件描述符类似于数组中的下标
 *
 *  https://juejin.im/entry/5b56f9045188251b157bb645
 *  https://www.cnblogs.com/Orgliny/articles/5699479.html
 *  同一进程的文件描述符指向了同一个打开的文件句柄: 可能是通过调用dup(), dup2() 或 fcntl形成的
 *  不同进程文件描述符指向了同一个打开的文件句柄: fork() 不同进程为父子关系或者通过套接字将打开的文件描述法传递
 *  两个不同的文件描述符, 若指向了同一文件句柄, 将共享同一文件偏移量.
 *  (相同进程多次打开同一文件时, 句柄是不同的.)
 *  文件描述符标志位进程和文件描述符私有, 对这一标志的修改不会影响同一进程或不同进程中的其他描述符
 *
 *  /dev/stdin,  /dev/fd/0对应的标准输入
 *  /dev/stdout, /dev/fd/1对应的标准输出
 *  /dev/stderr, /dev/fd/2对应的标准错误
 *  /proc/进程号/fd/n n是进程中打开的文件对应的文件描述符
 *  查看进程打开的文件数量: ls -l /proc/进程号/fd | wc -l (同一个文件, 多次打开, 文件句柄是不一样的)
 *
 *  文件相关系统调用

 *  open(...)
 *  read(...)
 *  write(...)
 *  lseek(...)
 *  close(...)
 *
 *  pread(int fd, void* buf, size_t count, off_t offset); 在指定的offset处进行读写，而且不会改变偏移量
 *  pwrite(int fd, void* buf, size_t count, off_t offset);
 *
 *  ssize_t readv(int fd, const struct iovec *iov, int iovcnt);  批量读取/写入
 *  ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
 *
 *  ssize_t preadv(int fd, const struct iovec *iov, int iovcnt);  指定offset处, 批量读取/写入
 *  ssize_t pwritev(int fd, const struct iovec *iov, int iovcnt);
 *
 *  若当前文件大于参数length, 丢弃超出的部分, 小于length, 调用将添加空字节或者一个文件空洞
 *  int truncate(const char* filename, off_t length);
 *  若当前文件大于参数length, 丢弃超出的部分, 小于length, 调用将添加空字节或者一个文件空洞或者返回错误
 *  int ftruncate(int fd, off_t length);
 */

// 以O_APPEND标志打开文件, 文件偏移至于起始处, 在写入数据, 数据会在哪个位置?
void o_append() {
    char file[] = "o_append.txt";
    int fd = open(file, O_CREAT | O_RDWR | O_APPEND | O_TRUNC, 0666);
    if (-1 == fd) {
        Exit("open error");
    }
    // 虽然偏移到了文件起点, 但是还是会写入到文件末尾
    // 设置了O_APPEND后，不管偏移到哪, 都会在文件末尾写数据
    // 即lseek对O_APPEND无效, 对READ有效
    char buf1[] = "1\n2\n";
    char buf2[] = "3\n4\n";
    char buf[3] = "";

    lseek(fd, 0, SEEK_SET);
    write(fd, buf1, (unsigned int)strlen(buf1));
    lseek(fd, 0, SEEK_SET);
    write(fd, buf2, (unsigned int)strlen(buf2));

    lseek(fd, 2, SEEK_SET);
    read(fd, buf, 2);
    printf("read = %s\n", buf);  // 2
    read(fd, buf, 2);
    printf("read = %s\n", buf);  // 3

    lseek(fd, 0, SEEK_SET);
    read(fd, buf, 2);
    printf("read = %s\n", buf);  // 文件起始处内容 1
    if (-1 == close(fd)) {
        Exit("close error");
    }
}

// 文件描述符及副本是否共享了文件偏移量和文件打开状态
void dup_() {
    char file[]= "dup_.txt";
    // fd1和fd2共享文件句柄, 包括偏移
    int fd1 = open(file, O_CREAT | O_RDWR | O_TRUNC, 0666);
    int fd2 = dup(fd1);
    int fd3 = open(file, O_RDWR);
    if (-1 == fd1 || -1 == fd2 || -1 == fd3) {
        Exit("open");
    }
    printf("fd1=%d, fd2=%d, fd3=%d\n", fd1, fd2, fd3);
    write(fd1, "a", 1);     // a
    write(fd2, "b", 1);     // ab, fd1和fd2共享文件偏移
    lseek(fd2, 0, SEEK_SET);
    write(fd1, "c", 1);     // cb
    write(fd3, "d", 1);     // db

    lseek(fd1, 0, SEEK_SET);
    char buf[4];
    buf[3] = buf[2] = '\0';

    read(fd1, buf, 2);
    printf("read = %s\n", buf);

    // 进程打开的文件
    char cmd[100];
    sprintf(cmd, "ls -l /proc/%d/fd", getpid());
    system(cmd);

    if (-1 == close(fd1) || -1 == close(fd3)) {
        Exit("close");
    }

    // fd1虽然已close, fd2可继续使用, 不受任何影响
    printf("write %d\n", (int)write(fd2, "a", 1));
    lseek(fd2, 0, SEEK_SET);
    read(fd2, buf, 3);
    printf("read = %s", buf);
    if (-1 == close(fd2)) {
        Exit("close");
    }
}

// fork与fd关系, 子进程与父进程共享文件偏移量
/*
 *  fork调用的一个奇妙之处就是它仅仅被调用一次, 却能够返回两次, 它可能有三种不同的返回值:
 *      在父进程中, fork返回新创建子进程的进程ID;
 *      在子进程中, fork返回0;
 *      如果出现错误, fork返回一个负值;
 *  返回值不同的原因: 其实就相当于链表, 进程形成了链表, 父进程的fork返回值指向子进程的进程id, 因为子进程没有子进程, 所以fork返回值为0.
 */
void fork_file() {
    char file[] = "fork.txt";
    int fd = open(file, O_CREAT | O_RDWR | O_TRUNC, 0666);
    if (-1 == fd) {
        Exit("exit");
    }

    char buf[100];
    pid_t pid = fork();
    if (pid < 0) {
        Exit("fork");
    }
    if (pid != 0) {
        sleep(1);
    }
    sprintf(buf, "pid=%d\n", getpid());
    write(fd, buf, strlen(buf));

    printf("pid=%d\n", getpid());
}

/*
 * 不同进程打开同一个文件
 * st: 每次写文件的挂起时间, 单位为秒
 */
void multi_process_file(unsigned int st) {
    char file1[] = "multi_process_file1.txt";
    char file2[] = "multi_process_file2.txt";
    int fd1 = open(file1, O_CREAT | O_RDWR, 0666);   // 多进程情况下会覆盖
    // O_APPEND 在文件尾部追加数据, 确保多个进程对同一文件追加数据时, 不会覆盖彼此的数据
    int fd2 = open(file2, O_CREAT | O_RDWR | O_APPEND, 0666);

    if (-1 == fd1 || -1 == fd2) {
        Exit("open");
    }

    char buf[100];
    sprintf(buf, "pid=%d\n", getpid());
    for(int i = 0; i < 10; i++) {
        sleep(st);
        write(fd1, buf, strlen(buf));
        write(fd2, buf, strlen(buf));
    }
    if (-1 == close(fd1) || -1 == close(fd2)) {
        Exit("close");
    }
}

// g++ ../../src/error_functions.cpp 5.cpp -I ../../include/
int main(int argc, char* argv[]) {
    if (argc > 1 && !strcmp("-h", argv[1])) {
        printf("argv[1]=\n"
               "        0:atomic_operation(argv[2])\n"
               "        1:file_mode()\n"
               "        2:o_append()\n"
               "        3:dup_()\n"
               "        4:fork_file()\n"
               "        5:multi_process_file(argv[2])\n");

        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):5;
    switch (type) {
        case 0:
            atomic_operation((uint)atoi(argv[2]));
            break;
        case 1:
            file_mode();
            break;
        case 2:
            o_append();
            break;
        case 3:
            dup_();
            break;
        case 4:
            fork_file();
            break;
        case 5:
            multi_process_file((uint)atoi(argv[2]));
            break;
        default:
            ;
    }
    return 0;
}