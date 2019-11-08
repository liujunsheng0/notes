#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <fcntl.h>       // 包含了读,写,关闭文件等操作的文件
#include <cstring>

#include "error_functions.h"

using namespace std;


#ifndef BUF_SIZE
#define BUF_SIZE 128
#endif

/*
 * 所有执行I/O操作的系统调用都以文件描述符(一个非负整数)来标识打开的文件(包括管道, socket, 终端, 普通文件等)
 * 针对每个进程, 文件描述符都自成一套
 * 文件描述符  用途     POSIX名称(unistd.h)    stdio流
 *   0       输入     STDIN_FILENO           stdin
 *   1       输出     STDOUT_FILENO          stdout
 *   2       错误     STDERR_FILENO          stderr
 *
 * 分配文件描述符的值为未使用的最小文件描述符
 * 文件描述符: 文件描述符表中的索引, 表中的值为文件指针
 */

void file_descriptor() {
    printf("file_descriptor in=%d, out=%d, err=%d\n\n", STDIN_FILENO, STDOUT_FILENO, STDERR_FILENO);
}

/*
 * 测试IO操作的四个主要系统调用
 * #include <unistd.h>
 * open flags参数值:
 *   O_RDONLY    以只读方式打开文件
 *   O_WRONLY    以只写方式打开文件
 *   O_RDWR      以读和写的方式打开文件
 * 上面三个只能选择一个, 下面的可以合理的任意组合:
 *
 *   O_APPEND    在文件尾部追加数据, 确保多个进程对同一文件追加数据时, 不会覆盖彼此的数据
 *   O_ASYNC     当I/O操作可行时, 产生信号通知进程, 仅对特定类型的文件有效, 如终端, socket

 *   O_CREAT     打开文件, 如果文件不存在则建立文件(检查文件是否存在和创建文件属于一个原子操作)
 *   O_EXCL      与O_CREAT配合使用, 如果文件存在, 则open()失败
 *
 *   O_TRUNC     如果文件存在且为普通文件, 清空文件内容, 将其长度置为0 (覆盖), truncate(截断)
 *
 *   O_DIRECT      无缓存的输入/输出
 *   O_DIRECTORY   如果参数非目录, 将返回错误
 *   O_DSYNC       根据同步I/O数据完整性的完成要求来执行文件写操作
 *   O_NONBLOCK    以非阻塞方式打开文件, 打开文件时可能阻塞, 如果未能立即打开文件, 返回错误; 成功后, 后续的IO操作也是非
 *                 阻塞的, 若系统调用未能立即完成，则可能只会传输部分数据或失败
 *   O_SYNC        以同步I/O方式打开文件
 *
 */

// 返回打开的文件描述符
int open_file(const string &filename, int flag, mode_t mode=0666) {
    /*
     * open(const char* filename, int flags, ...(mode_t mode))
     * return:
     *      成功: 返回文件描述符, 用以指代打开的文件, 取值为未使用的文件描述符中的最小值
     *      失败: 返回-1, errno置为相应的错误标志
     * flags: 掩码, 指定文件的访问模式
     * mode:  指定文件的访问权限(如果非新建文件, 该参数可省略) 如0666 表示 -rw-rw–rw–
     */
    int fd = open(filename.data(), flag, mode); // 文件名, 文件打开方式, 返回文件描述符, 错误返回-1, 详细错误见errno
    if (-1 == fd) {
        Exit("open file: %s error", filename.data());
    }
    return fd;
}

// 对于每个打开的文件, 内核会记录其文件偏移
void lseek_file(int fd, int offset, int whence=SEEK_CUR) {
    /*
     * off_t lseek(int fd, off_t offset, int whence)
     * offset: 偏移的字节数
     * whence: SEEK_SET  从文件开始
     *         SEEK_CUR  从当前位置开始
     *         SEEK_END  将文件偏移设置为起始于文件尾部的offset个字节, 也就是说offset从文件的最后一个字节之后的下一个字节算起
     */
    if (lseek(fd, offset, whence)  == -1) {
        Exit("lseek error");
    }
}


void read_file(int fd) {
    /*
     * ssize_t read(int fd, void* buf, size_t buf_size)
     * return:
     *      成功: 返回读取的字节数, 如果遇到文件结束(EOF)返回0
     *      失败: -1, errno置为相应的错误号
     */
    char buf[BUF_SIZE + 1];  // 留一个字节置'/0'
    buf[BUF_SIZE] = '\0';
    while (true) {
        ssize_t num_read = read(fd, buf, BUF_SIZE);   // 返回读取的字节数量, 文件结束返回0, 错误返回-1
        if (num_read < BUF_SIZE) {
            buf[num_read] = '\0';
        }
        if (num_read == 0) {
            break;
        }
        if (num_read == -1) {
            Exit("read error");
        }
        cout<<"read num="<<num_read<<"bytes, content:\n"<<buf<<endl;
    }
}

void write_file(int fd, char* buf, size_t buf_size) {
    /*
     * ssize_t write(int fd, void* buf, size_t count)
     * return:
     *      成功: 返回写入的字节数
     *           如果写入的字节数小于count, 可能是因为磁盘已满, 或者是进程资源对文件大小的限制
     *      失败: -1, errno置为相应的错误号
     */
    ssize_t write_num = write(fd, buf, (unsigned int)buf_size);
    if (write_num != buf_size) {
        Exit("write error");
    }
}

void close_file(int fd, const string &filename) {
    /*
     * 释放描述符以及相关的内核资源
     * int close(int fd)
     * return: 成功: 0; 失败: -1
     */
    if (close(fd) != 0) {
        Exit("close file:%s error", filename.data());
    }
}

void system_call_file_io() {
    string filename = "test.txt";
    char input[] = "0123456789";
    int fd = open_file(filename, O_RDWR | O_CREAT);
    write_file(fd, input, 10);
    lseek_file(fd, 1, SEEK_SET);
    read_file(fd);
    close_file(fd, filename);
}

/* 文件空洞 https://blog.csdn.net/clamercoder/article/details/38361815
 *          https://blog.csdn.net/shenlanzifa/article/details/44016537
 *  文件偏移量跨越了文件结尾, 执行read操作返回0, 执行write操作是可以写入数据的.
 *  从文件结尾到新写入数据间的这段空间称为文件空洞, 从编程角度来看, 文件空洞中存在字节, 只不过是空字节.
 *  文件空洞不占用任何磁盘空间, 直至像文件空洞后面的偏移写入数据, 系统才会为其分配空间.
 *  文件空洞的逻辑大小一般比占用的磁盘大小要大的多
 *
 *  查看系统block size tune2fs -l /dev/sda1|grep "Block size"
 *
 *  空洞文件的特点: offset > 实际文件大小
 *  作用: 如空洞文件作用很大, 例如迅雷下载文件, 在未下载完成时就已经占据了全部文件大小的空间, 这时候就是空洞文件.
 *  ls -l file        查看文件逻辑大小
 *  du -c file        查看文件实际占用的存储块多少
 *  od -c file        查看文件存储的内容
 */

void file_hole() {
    string file1 = "file_hole_write.txt";
    string file2 = "file_hole_no_write.txt";
    string file3 = "file_no_hole.txt";

    remove(file1.data());
    remove(file2.data());
    remove(file3.data());

    int fd1 = open_file(file1, O_WRONLY | O_CREAT);
    int fd2 = open_file(file2, O_WRONLY | O_CREAT) ;
    int fd3 = open_file(file3, O_WRONLY | O_CREAT);
    long offset = 4096 * 100;
    lseek(fd1, offset, SEEK_SET);
    lseek(fd2, offset, SEEK_SET);

    char buf1[] = "1";
    write_file(fd1, buf1, (unsigned int)(strlen(buf1)));
    write_file(fd3, buf1, (unsigned int)(strlen(buf1)));
    int tmp;
    cout<<"pid="<<getpid()<<"\ninput anything continue";
    char cmd[100] = "";
    // 进程打开的文件
    sprintf(cmd, "ls -l /proc/%d/fd", getpid());
    system(cmd);

    scanf("%d", &tmp);
    close(fd1);
    close(fd2);
    close(fd3);

    cout<<endl<<"bytes\n";

    system("du -b file_hole_write.txt");
    system("du -b file_hole_no_write.txt");
    system("du -b file_no_hole.txt");

    cout<<"block size\n";
    system("du -c file_hole_write.txt | grep file");
    system("du -c file_hole_no_write.txt | grep file");
    system("du -c file_no_hole.txt | grep file");

}

// g++ ../../src/error_functions.cpp file.cpp -I ../../include/
int main(int argc, char *argv[]) {
    if (argc > 1 && !strcmp("-h", argv[1])) {
        printf("argv[1]=\n"
               "        0: file_descriptor()\n"
               "        1: system_call_file_io()\n"
               "        2: file_hole()\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            file_descriptor();
            break;
        case 1:
            system_call_file_io();
            break;
        case 2:
            file_hole();
            break;
        default:
            ;
    }
    return 0;
}