/*
 * 文件I/O缓冲
 *
 * read()和write()系统调用在操作磁盘文件时不会直接发起磁盘访问, 仅仅在用户空间缓冲区与内核缓存区之间复制数据
 * read和write共用一块缓冲空间
 * 如:
 *      write(fd, "abc", 3); 将三个字节的数据从用户空间内存传递到内核缓冲区, write立即返回, 在后续某个时刻, 内核会将
 *      内核缓冲区的数据写入磁盘(因此可以说系统调用与磁盘操作并不同步).
 *      如果在此期间, 另一个进程试图读取文件的这几个字节, 内核会从内核缓冲区提供这些数据.
 *
 *      read(fd, buf, 3); 内核从磁盘中读取数据并存储到内核缓冲区. read()从内核缓冲区中读取数据, 直至把缓冲区的数据读完,
 *      这时, 内核会将文件的下一段内容读入内和缓冲区(内核一般会执行预读)
 *
 *      采用这一设计, 使read()和write()调用更为快速, 因为不需要等待磁盘操作, 同时减少了内核必须执行的磁盘传输次数.
 *
 *      Linux内核对缓冲区告诉缓存的大小没有固定上限, 内核会分配尽可能多的缓冲区高速缓存页.
 *
 *      内核缓存区仅受限于两个因素: 可以的物理内存总量; 出于其他目的对物理内存的需求.若可用内存不足, 则内核会将一些修改
 *      过的缓冲区刷新到磁盘, 并释放供系统使用
 *
 * stdio库函数使用了用户缓冲区, 减少了系统调用次数.
 * 系统在每个缓冲区中将数据向磁盘传递时会把程序阻塞起来
 *
 * 写文件过程: stdio缓冲 -> 内核缓冲 -> 磁盘
 *
 * 控制文件I/O的内核缓冲
 * 同步I/O数据完整性和同步I/O文件完整性
 *      区别: 用于描述文件的元数据, 即内核针对文件而存储的数据
 *      文件元数据: 文件属主, 属组, 权限, 大小, 文件链接数量, 文件最近访问, 修改, 以及元数据发生变化的时间戳,
 *                  指向文件数据块的指针等.
 * 同步I/O数据完整性(synchronized IO data integrity completion)
 *      确保针对文件的一次更新传递了"足够的"信息（部分文件元数据）到磁盘, 以便于之后对数据的获取. 
 *      部分元数据是指用于获取数据的文件元数据
 * 同步I/O文件完整性(synchronized IO file integrity completion)
 *      确保针对文件的一次更新传递了"所有的"信息（所有文件元数据）到磁盘, 即使有些在后续对文件数据的操作并不需要.
 *
 * 用于控制文件I/O系统缓冲的系统调用
 * #include<unistd.h>
 * int fsync(int fd); 成功:0; 失败: -1
 *      将缓存数据和打开的文件描述法fd相关的所有元数据都刷新到磁盘
 *      调用fsync会强制使文件处于 同步I/O文件完整性 状态
 *      返回时间: 仅在对磁盘设备（或者至少是其高速缓存）的传递完成后, fsync()调用才会返回
 * int fdatasync(int fd);  成功:0; 失败: -1
 *       作用类似于fsync(), 只是调用fdatasync会强制使文件处于 同步I/O数据完整性状态
 *       与fsync的区别: fdatasync()可能会减少磁盘操作的次数, 由fsync()调用请求的两次变成一次.例如, 修改了文件的数据,
 *                      而文件大小不变, 那么调用fdatasync()调用请求只强制进行了数据更新, 相比之下, fsync()调用会强制将
 *                      元数据传递到磁盘上, 而元数据和文件数据通常驻留在磁盘的不同区域, 更新这些数据需要反复在整个磁盘
 *                      上执行寻道操作, 适用于对性能要求较高的应用.
 *                      (针对同步I/O数据完整性状态, 如果是注入修改时间戳之类的元数据属性发生了变化, 无需传递到磁盘,
 *                      只要是不影响数据完整的元数据都无需传递到磁盘)
 * void sync();
 *      使包含更新文件信息的所有内核缓冲区（即数据块、指针块、元数据等）刷新到磁盘上
 *      返回时间: 仅在所有数据已传递到磁盘上时返回
 *      若内容发生变化的内核缓冲区在30s内未经显式方式同步到磁盘上, 则一条长期运行的内核线程会确保将其刷新到磁盘上.
 *      这一做法是为了规避缓冲区与相关磁盘文件内容长期处于不一致状态.
 *
 * 使所有写入同步: O_SYNC
 *      调用open函数时, 如果指定了O_SYNC标志, 每个write()调用会自动将文件数据和元数据刷新到磁盘上.(即按照同步I/O文件完
 *      整性的要求执行写操作)
 * O_DSYBC: 按照同步I/O数据完整性的要求来执行写操作,
 * O_RSYNC: 与O_SYNC和O_DSYNC标志配合使用
 *      O_RSYNC, O_DSYNC: 按照同步I/O数据完整性的要求来执行读操作
 *      O_RSYNC, O_SYNC: 按照同步I/O文件完整性的要求来执行读操作
 *  O_DIRECT: 不使用内核缓冲取, 直接对磁盘进行I/O, 但是性能较差
 *      直接IO的限制:
 *          1. 用于传递数据的缓冲区, 内存边界必须对齐为块大小的整数倍
 *          2. 文件和设备的偏移量, 必须是块大小的整数倍;
 *          3. 待传递数据的长度必须是块大小的整数倍
 *      不遵守上述限制, 将会导致EINVAL错误
 *
 *  IO缓冲层次关系
 *      首先 , 通过stdio库将用户数据传递到stdio缓冲区 , 该缓冲区位于用户态内存区 
 *      当缓冲区填满 , stdio库会调用write()系统调用 , 将数据传递到内核高速缓冲区 , 该缓冲区位于内核态内存区
 *      最终 , 内核发起磁盘操作
 *
 *  就I/O模式向内核提出建议
 *  posix_fadvise()系统调用允许进程就自身访问文件时可能采取的模式通知内核
 *  #define _XOPEN_SOURCE 600
 *  #include <fcntl.h>
 *  int posix_fadvise(int fd, off_t offset, off_t len, int advice); 成功:0; 失败:正数
 *      根据posix_fadvise()提供的信息优化对内核缓冲区的使用, 进而提高性能
 *      fd:文件描述符
 *      offset, len确定了建议适用的文件区域, offset表示区域起始的偏移量, len指定了区域的大小, len为0表示从offset开始至文件结尾
 *      advice表示进程对文件采取的访问模式
 *          POSIX_FADV_NORMAL, 默认行为, 将文件预读窗口大小设置为默认值128kb
 *          POSIX_FADV_SEQUENTIAL, 将文件预读窗口大小设置为默认值的两倍
 *          POSIX_FADV_RANDOM, 禁用文件预读
 *          POSIX_FADV_WILLNEED ....
 */


#include <stdio.h>
#include <unistd.h>
#include "error_functions.h"
/*
 * 库函数
 *  setvbuf(File *stream, char *buf, int mode, size_t size);
 *      控制stdio库使用缓冲的形式,  成功: 0; 失败: 非0 (用户空间缓冲区)
 *      打开流后, 必须在调用其他stdio函数前先调用setvbuf(), setvbuf()调用将影响后续在指定流上进行的所有stdio操作
 *      buf和size指定了stream要使用的缓存区
 *      mode指定了缓冲类型, 并具有下列值之一:
 *          _IONBF: 不对IO进行缓冲, buf, size = NULL, 0
 *          _IOLBF: 行缓冲, 每次读取一行数据, 以换行符作为结束标志
 *          _IOFBF: 采用全缓冲,  单词读, 写数据的大小与缓冲区相同, 默认模式
 *  setbuf(File *stream, char *buf)
 *      等价于setvbuf(fp, buf, (buf != NULL)? _IOFBF: _IONBF, BUFSIZE);
 *
 *  int fflush(File *stream);
 *      将stdio输出流中的数据刷新到内核缓冲区,同时刷新stream的输出缓冲区 成功: 0 失败: -1
 *      如果stream为NULL, fflush()将刷新所有缓冲区
 *
 */
void setvbuf_test() {
    size_t buf_size = 8;
    char buf[buf_size + 1] = {'\0'};

    FILE* fp = fopen("../data/13_1.txt", "w+");
    if (fp == NULL) {
        Exit("open error");
    }
    if (setvbuf(fp, buf, _IOFBF, buf_size) != 0) {
        Exit("setvbuf error");
    }
    // 超过八个字节, 输出到文件
    char words[] = "12345678abcdef";
    for(int i = 0; i < (sizeof(words) - 2); i += 2) {
        fwrite(words + i, 1, 2, fp);
        printf("i=%d, buf=%s\n", i, buf);
    }
//    fflush(fp);
    int tmp;
    scanf("%d", &tmp); // 此时查看13_1.txt为12345678

    // read和write共用一块缓冲区
    fseek(fp, 0, SEEK_SET);
    char read_buf[4] = {'\0'};
    fread(read_buf, 1, 3, fp); // 此时查看13_1.txt为12345678abcdef
    printf("buf=%s, read_buf=%s\n", buf, read_buf); // buf 由 abcdefgh->12345678

    if (fclose(fp) != 0) {
        Exit("close error");
    }
}

/*
 * 若打开一个流同时用于输入和输出, C99标准提出:
 * 1. 输出操作不能紧跟一个输入操作, 必须在二者之间调用fflush()函数或者文件定位函数,如fseek
 * 2. 输入操作不能紧跟一个输出操作, 必须在二者之间调用一个文件定位函数.
 */

void test_write_read() {
    FILE* fp = fopen("../data/13_2.txt", "w+");
    if (fp == NULL) {
        Exit("open error");
    }
    char buf[3] = {'a', 'b', '\0'};
    char read[3] = {'\0'};
    if (setvbuf(fp, buf, _IOFBF, 2) != 0) {
        Exit("setvbuf error");
    }
    fwrite("1", 1, 1, fp);
    fwrite("2", 1, 1, fp);
    fwrite("3", 1, 1, fp);
    fread(read, 1, 2, fp); // 此时文件结果多了个字符2, 错误的
    printf("%s\n", read);
    fclose(fp);
}

/*
 * 混合使用库函数和系统调用进行文件IO可能带来的问题
 * #include <stdio.h>
 * int fileno(File *stream); 返回相应的文件描述符
 * File *fdopen(int fd, const char *mode); 给定文件描述符, 创建相应的流, mode为"r/w/a"等模式
 */
void test() {
    // 通常情况下printf函数的输出会在write()函数的输出之后出现, 因为stdio使用了用户空间的缓冲区.
    // 可以使用fflush()来规避这样的问题
    printf("stdio printf");
    write(STDOUT_FILENO, "hello system call\n", 17);
}

int main() {
//    setvbuf_test();
//    test_write_read();
    test();
    return 0;
}