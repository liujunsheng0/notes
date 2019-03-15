/*
 * 所有执行I/OC操作的系统调用都以文件描述符(一个非负整数)来标识打开的文件(包括管道, socket, 终端, 普通文件等)
 * 文件描述符  用途     POSIX名称(unistd.h)    stdio流
 *   0       输入     STDIN_FILENO           stdin
 *   1       输出     STDOUT_FILENO          stdout
 *   2       错误     STDERR_FILENO          stderr
 *
 *   文件描述符的值为未使用的最小文件描述符
 */


#include <iostream>
#include <unistd.h>
#include <fcntl.h>       // 包含了读,写,关闭文件等操作的文件

//#include "header.h"
#include "error_functions.h"

using namespace std;


#ifndef BUF_SIZE
#define BUF_SIZE 1024
#endif

// 文件描述符
void file_descriptor() {
    printf("file_descriptor in=%d, out=%d, err=%d\n\n", STDIN_FILENO, STDOUT_FILENO, STDERR_FILENO);
}

/*
 * 测试IO操作的四个主要系统调用
 * #include <unistd.h>
 * off_t lseek(int fd, off_t offset, int whence)
 * offset: 偏移的字节数
 * whence: SEEK_SET  从文件开始
 *         SEEK_CUR  从当前位置开始
 *         SEEK_END  将文件偏移设置为起始于文件尾部的offset个字节, 也就是说offset从文件的最后一个字节之后的下一个字节算起
 * open flags参数值:
 *   O_RDONLY    以只读方式打开文件
 *   O_WRONLY    以只写方式打开文件
 *   O_RDWR      以读和写的方式打开文件
 * 上面三个只能选择一个, 下面的可以合理的任意组合:

 *   O_CREAT     打开文件, 如果文件不存在则建立文件
 *   O_EXCL      与O_CREAT配合使用, 如果文件存在, 则open()失败
 *
 *   O_DIRECT      无缓存的输入/输出
 *   O_DIRECTORY   如果参数非目录, 将返回错误
 *   O_TRUNC     如果文件以及存在且未普通文件, 清空文件内容, 将其长度置为0 (覆盖), truncate(截断)
 *   O_APPEND    在文件尾部追加数据, 确保多个进程对同一文件追加数据时, 不会覆盖彼此的数据
 *   O_ASYNC       当I/O操作可行时, 产生信号通知进程, 仅对特定类型的文件有效, 如终端, socket
 *   O_DSYNC       根据同步I/O数据完整性的完成要求来执行文件写操作
 *   O_NONBLOCK    以非阻塞方式打开文件, 打开文件时可能阻塞, 如果未能立即打开文件, 返回错误; 成功后, 后续的IO操作也是非
 *                 阻塞的, 若系统调用未能立即完成，则可能只会传输部分数据或失败
 *   O_SYNC        以同步I/O方式打开文件
 *
 */

int open_file(string filename, int open_flag) {
    int fd = open(filename.data(), open_flag); // 文件名, 文件打开方式, 返回文件描述符, 错误返回-1, 详细错误见errno
    if (fd == -1) {
        errExit("open file: %s error", filename.data());
    }
    printf("open file: %s success, fd=%d\n", filename.data(), fd);
    return fd;
}

void read_file(int fd) {
    char buf[BUF_SIZE + 1];  // 留一个字节置‘/0’
    buf[BUF_SIZE] = '\0';
    while (true) {
        ssize_t num_read = read(fd, buf, BUF_SIZE);   // 返回读取的字节数量, 文件结束返回0, 错误返回-1
        if (num_read < BUF_SIZE) {
            buf[num_read] = '\0';
        }
        // lseek(fd, 1, SEEK_CUR); //  文件偏移一个字节
        if (num_read == 0) {
            break;
        }
        if (num_read == -1) {
            errExit("read error");
        }
        cout<<"num_read="<<num_read<<" buf="<<buf<<endl;
    }
}

void lseek_file(int fd, int offset, int whence) {
    if (lseek(fd, offset, whence)  == -1) {
        errExit("lseek error");
    }
}

void write_file(int fd, char* buf, size_t buf_size) {
    int write_num = write(fd, buf, (unsigned int)buf_size);
    cout<<"write bytes= "<<write_num<<endl;
}

void close_file(int fd, string filename) {
    if (close(fd) != 0) {
        errExit("close file:%s error", filename.data());
    }
}

void system_call_file_io() {
    string filename = "../main.cpp";
    int fd = open_file(filename, O_RDONLY);
    read_file(fd);
    close_file(fd, filename);

}

/* 文件空洞 https://blog.csdn.net/clamercoder/article/details/38361815
 *          https://blog.csdn.net/shenlanzifa/article/details/44016537
 *  文件偏移量跨越了文件结尾, 执行read操作返回0, 执行write操作是可以写入数据的.
 *  从文件结尾到新写入数据间的这段空间称为文件空洞, 从编程角度来看, 文件空洞中存在字节, 只不过是空字节.
 *  文件空洞不占用任何磁盘空间, 直至像文件空洞后面的偏移写入数据, 系统才会为其分配空间.
 *
 *  空洞文件的特点: offset > 实际文件大小
 *  作用: 如空洞文件作用很大, 例如迅雷下载文件, 在未下载完成时就已经占据了全部文件大小的空间, 这时候就是空洞文件.
 *  ls -l file        查看文件逻辑大小
 *  du -c file        查看文件实际占用的存储块多少
 *  od -c file        查看文件存储的内容
 */

void file_hole() {
    string file1 = "../data/file_hole_write.txt";
    string file2 = "../data/file_hole_no_write.txt";
    string file3 = "../data/file_no_hole.txt";

    int fd1 = open_file(file1, O_WRONLY | O_CREAT);
    int fd2 = open_file(file2, O_WRONLY | O_CREAT) ;
    int fd3 = open_file(file3, O_WRONLY | O_CREAT);
    long offset = 1024 * 1024 * 1;
    lseek(fd1, offset, SEEK_SET);
    lseek(fd2, offset, SEEK_SET);

    char buf1[] = "123456789";
    write_file(fd1, buf1, (unsigned int)(strlen(buf1)));
    write_file(fd3, buf1, (unsigned int)(strlen(buf1)));
    close(fd1);
    close(fd2);
    close(fd3);
}

int get_file_bytes(string filename) {
    FILE* fd = fopen(filename.data(), "rb");
    if (fd == NULL) {
        errExit("open file: %s error", filename.data());
    }
    fseek(fd, 0, SEEK_END);
    fclose(fd);
    return ftell(fd);
}

void read_file_hole() {
    string file1 = "../data/file_hole_write.txt";
    string file2 = "../data/file_hole_no_write.txt";
    string file3 = "../data/file_no_hole.txt";
    // size(字节数): f1=8192009, f2=0, f3=9
    printf("size: f1=%d, f2=%d, f3=%d\n", get_file_bytes(file1), get_file_bytes(file2), get_file_bytes(file3));
}

int main() {
//    file_descriptor();
//    system_call_file_io();
    file_hole();
    read_file_hole();
    return 0;
}