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

#include "header.h"
#include "error_functions.h"

using namespace std;


#ifndef BUF_SIZE
#define BUF_SIZE 32
#endif

// 文件描述符
void file_descriptor() {
    printf("file_descriptor in=%d, out=%d, err=%d\n\n", STDIN_FILENO, STDOUT_FILENO, STDERR_FILENO);
}

/*
 * 测试IO操作的四个主要系统调用
 * #include <unistd.h>
 * off_t lseek(int fd, off_t offset, int whence)
 * offset: 便宜的字节数
 * whence: SEEK_SET  从文件开始
 *         SEEK_CUR  从当前位置开始
 *         SEEK_END  将文件偏移设置为起始于文件尾部的offset个字节, 也就是说offset从文件的最后一个字节之后的下一个字节算起
 */
void system_call_file_io() {
    string filename = "../main.cpp";
    int fd = open(filename.data(), O_RDONLY); // 文件名, 文件打开方式, 返回文件描述符, 错误返回-1, 详细错误见errno
    if (fd == -1) {
        errExit("open file: %s error", filename.data());
    }
    printf("open file: %s success, fd=%d\n", filename.data(), fd);

    char buf[BUF_SIZE + 1];  // 留一个字节置‘/0’
    buf[BUF_SIZE] = '\0';
    while (TRUE) {
        ssize_t num_read = read(fd, buf, BUF_SIZE);   // 返回读取的字节数量, 文件结束返回0, 错误返回-1
        if (num_read < BUF_SIZE) {
            buf[num_read] = '\0';
        }
//         lseek(fd, 1, SEEK_CUR); //  文件偏移一个字节
        if (num_read == 0) {
            break;
        }
        if (num_read == -1) {
            errExit("read error");
        }
        cout<<"num_read="<<num_read<<" buf="<<buf<<endl;
    }
    if (close(fd) != 0) {
        errExit("close file:%s error", filename.data());
    }
}

/* 文件空洞 https://blog.csdn.net/clamercoder/article/details/38361815
 *        https://blog.csdn.net/shenlanzifa/article/details/44016537
 *  文件偏移量跨越了文件结尾, 执行read操作返回0, 执行write操作是可以写入数据的.
 *  从文件结尾到新写入数据间的这段空间称为文件空洞, 从编程角度来看, 文件空洞中存在字节, 只不过是空字节.
 *  文件空洞不占用任何磁盘空间, 直至像文件空洞中写入数据时, 系统才会为止分配空间.
 *
 */

void file_hole() {
    string file1 = "../data/file_hole1.txt";
    string file2 = "../data/file_hole2.txt";
    int fd1 = open(file1.data(), O_WRONLY | O_CREAT);
    int fd2 = open(file2.data(), O_WRONLY | O_CREAT);
    int offset = 102400000000;
    lseek(fd1, offset, SEEK_SET);
    lseek(fd2, offset, SEEK_SET);

    char buf1[] = "123456789";
    int write_num = write(fd1, buf1, strlen(buf1));
    cout<<"write_num = "<<write_num<<endl;

    if (close(fd1) != 0) {
        errExit("close file:%s error", file1.data());
    }
    if (close(fd2) != 0) {
        errExit("close file:%s error", file1.data());
    }
}


void read_file_hole() {
    string file1 = "../data/file_hole1.txt";
    string file2 = "../data/file_hole2.txt";
    int fd = open(file1.data(), O_RDONLY);
    char buf[BUF_SIZE + 1];  // 留一个字节置‘/0’
    buf[BUF_SIZE] = '\0';

    while (TRUE) {
        ssize_t num_read = read(fd, buf, BUF_SIZE);
        if (num_read > 0 and num_read < BUF_SIZE) {
            buf[num_read] = '\0';
        }
        if (num_read == 0) {
            break;
        }
        if (num_read == -1) {
            break;
        }
        cout<<"num_read="<<num_read<<" buf="<<buf<<endl;
    }
}

int main() {
//    file_descriptor();
//    system_call_file_io();
//    file_hole();
    read_file_hole();
    return 0;
}