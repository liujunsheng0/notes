// Linux 系统编程手册 第13章 文件I/O缓冲
#include "header.h"
#include "error_functions.h"
#include <iostream>
using namespace std;
/*
 * 文件I/O缓冲
 *
 * 出于速度和效率考虑, 系统IO(内核缓冲区)和标准C语言库IO(用户态缓冲区)在操作磁盘文件时会对数据进行缓冲.
 *
 * 内核缓冲:
 *      read()和write()系统调用在操作磁盘文件时不会直接发起磁盘访问, 仅仅在用户空间缓冲区与内核缓存区之间复制数据.
 *      (read和write共用一块缓冲空间)
 *      如 write(fd, "abc", 3)
 *        将三个字节的数据从用户空间内存传递到内核缓冲区, write立即返回, 在后续某个时刻, 内核会将内核缓冲区的数据写入磁盘
 *        (因此可以说系统调用与磁盘操作并不同步). 如果在此期间, 另一个进程试图读取文件的这几个字节, 内核会从内核缓冲区提供这些数据.
 *
 *        read(fd, buf, 3)
 *        内核从磁盘中读取数据并存储到内核缓冲区. read()从内核缓冲区中读取数据, 直至把缓冲区的数据读完,
 *        这时, 内核会将文件的下一段内容读入内和缓冲区(内核一般会执行预读)
 *
 *      采用这一设计, 使read()和write()调用更为快速, 因为不需要等待磁盘操作, 同时减少了内核必须执行的磁盘传输次数.
 *
 *      Linux内核对缓冲区告诉缓存的大小没有固定上限, 内核会分配尽可能多的缓冲区高速缓存页.
 *
 *      内核缓存区仅受限于两个因素: 可以的物理内存总量; 出于其他目的对物理内存的需求.若可用内存不足, 则内核会将一些修改
 *      过的缓冲区刷新到磁盘, 并释放供系统使用
 *
 * 用户态缓冲区
 *      stdio库函数使用了用户缓冲区, 减少了系统调用次数.
 *      系统在每个缓冲区中将数据向磁盘传递时会把程序阻塞起来
 *
 * 写文件过程: stdio缓冲(用户态缓冲区) -> 内核缓冲 -> 磁盘
 *      首先, 通过stdio库将用户数据传递到stdio缓冲区, 该缓冲区位于用户态内存区;
 *      当缓冲区填满, stdio库会调用write()系统调用, 将数据传递到内核高速缓冲区, 该缓冲区位于内核态内存区
 *      最终, 内核发起磁盘操作
 *
 * 使所有写入同步
 *      O_SYNC : 调用open函数时, 如果指定了O_SYNC, write()会自动将文件数据和元数据刷新到磁盘上.(按照同步I/O文件完整性的要求执行写操作)
 *      O_DSYBC: 与O_SYNC类似, 不过是按照同步I/O数据完整性的要求来执行写操作,
 *      O_RSYNC: 与O_SYNC和O_DSYNC标志配合使用
 *
 *      O_RSYNC, O_DSYNC: 按照同步I/O数据完整性的要求来执行读操作
 *      O_RSYNC, O_SYNC: 按照同步I/O文件完整性的要求来执行读操作
 *
 *  O_DIRECT: 不使用内核缓冲取, 直接对磁盘进行I/O, 但是性能较差
 *      直接IO的限制:
 *          1. 用于传递数据的缓冲区, 内存边界必须对齐为块大小的整数倍
 *          2. 文件和设备的偏移量, 必须是块大小的整数倍;
 *          3. 待传递数据的长度必须是块大小的整数倍
 *      不遵守上述限制, 将会导致EINVAL错误
 */

/*
 * 用户态缓冲区
 * 当操作磁盘文件时, 缓冲可以减少系统调用, 如C函数库的fprintf(), fgets()等, 使用stdio库可以使程序员免于自行处理数据缓冲
 *
 * 设置stdio流的缓冲模式(用户态缓冲)
 *      int setvbuf(File *stream, char *buf, int mode, size_t size);
 *          设置stdio库使用缓冲的形式,  成功: 0; 失败: 非0 (用户空间缓冲区)
 *          打开流后, 必须在调用其他stdio函数前先调用setvbuf(), setvbuf()调用将影响后续在指定流上进行的所有stdio操作
 *
 *          buf和size指定了stream要使用的缓存区
 *          mode指定了缓冲类型, 并具有下列值之一:
 *              _IONBF: 不对IO进行缓冲, 立即调用相应的系统调用, buf, size = NULL, 0
 *              _IOLBF: 行缓冲, 每次读取一行数据, 以换行符作为结束标志
 *              _IOFBF: 采用全缓冲,  单词读, 写数据的大小与缓冲区相同(缓冲区满了以后调用相应的系统调用), 默认模式
 *
 *      int setbuf(File *stream, char *buf)
 *          等价于setvbuf(fp, buf, (buf != NULL)? _IOFBF: _IONBF, BUFSIZE);
 *
 *  int fflush(File *stream);
 *      将stdio输出流中的数据刷新到内核缓冲区,同时刷新stream的输出缓冲区 成功: 0 失败: -1
 *      如果stream为NULL, fflush()将刷新所有缓冲区
 *  当关闭相应流时, 将自动刷新stdio缓冲区
 */
void user_buffer() {
    char buf[9] = {'\0'};
    char cmd[] = R"(echo "cat user_buffer.txt -> \c" && cat user_buffer.txt && echo "")";
    FILE* fp = fopen("user_buffer.txt", "w+");

    if (nullptr == fp) {
        Exit("open error");
    }
    if (setvbuf(fp, buf, _IOFBF, 8) != 0) {
        Exit("setvbuf error");
    }

    char words[] = "001234567800abcdefhi00123456";
    // TODO:: 缓冲区为空, 首次写入时会立马更新到磁盘文件, why??
    for(int i = 0; i < (sizeof(words) / 2); i++) {
        if (2 != fwrite(words + i * 2, 1, 2, fp)) {
            Exit("fwrite");
        }
        printf("offset=%-2d, write=%c%c, buf=%s\n", i * 2, words[i * 2], words[i * 2 + 1], buf);
        if (i % 5 == 0 || i % 4 == 0) {
            // 查看文件内容, 缓冲区未满时, 不会将数据刷新到磁盘文件
            system(cmd);
            printf("\n");
        }
    }
    // 查看文件内容
    system(cmd);
    printf("\nafter fflush\n");
    // 用户态缓冲区数据刷新到磁盘
    fflush(fp);
    // 查看文件内容
    system(cmd);
    printf("\n");

    // read和write共用一块缓冲区
    fseek(fp, 0, SEEK_SET);
    char read_buf[3] = {'\0'};
    if (2 != fread(read_buf, 1, 2, fp)) {
        Exit("fread");
    }
    // 预读缓冲区大小的数据, 空间局部性原则
    printf("buf=%s, read_buf=%s\n", buf, read_buf); // buf 由 abcdefgh->12345678

    if (fclose(fp) != 0) {
        Exit("close error");
    }
}


/*
 * 内核缓冲
 *
 * 同步I/O *数据* 完整性和同步I/O *文件* 完整性
 *      区别: 用于描述文件的元数据, 即内核针对文件而存储的数据, 文件完整性存储的元数据更多
 *      文件元数据: 文件属主, 属组, 权限, 大小, 文件链接数量, 文件最近访问, 修改, 以及元数据发生变化的时间戳, 指向文件数据块的指针等.
 *      同步IO数据完整性是文件完整性的子集
 *
 * 同步IO 数据 完整性 (synchronized IO data integrity completion)
 *      确保针对文件的一次更新传递了"足够的"信息（部分文件元数据）到磁盘, 以便于之后对数据的获取.
 *      (只传递以后对读操作中需要的元数据)
 *
 * 同步IO 文件 完整性(synchronized IO file integrity completion)
 *      确保针对文件的一次更新中, 将"所有发生更新的文件元数据"到磁盘, 即使有些在后续对文件数据的读操作中并不需要.
 *
 * int fsync(int fd); 成功:0; 失败: -1
 *      将缓存数据和打开的文件描述法fd相关的所有元数据都刷新到磁盘
 *      调用fsync会强制使文件处于 同步I/O文件完整性 状态
 *      返回时间: 仅在对磁盘设备（或者至少是其高速缓存）的传递完成后, fsync()调用才会返回
 *
 * int fdatasync(int fd);  成功:0; 失败: -1
 *      作用类似于fsync(), 只是调用fdatasync会强制使文件处于 同步I/O数据完整性状态
 *
 * void sync();
 *      将包含更新文件信息的所有内核缓冲区（即数据块、指针块、元数据等）刷新到磁盘上
 *      返回时间: 仅在所有数据已传递到磁盘上时返回
 */

/*
 * 若打开一个流同时用于输入和输出, C99标准提出:
 * 1. 输出操作不能紧跟一个输入操作, 必须在二者之间调用fflush()函数或者文件定位函数,如fseek
 * 2. 输入操作不能紧跟一个输出操作, 必须在二者之间调用一个文件定位函数.
 */
void write_and_read() {
    FILE* fp = fopen("write_read.txt", "w+");
    if (fp == nullptr) {
        Exit("fopen");
    }
    char buf[4] = {'\0'};
    char read[3] = {'\0'};
    if (setvbuf(fp, buf, _IOFBF, 2) != 0) {
        Exit("setvbuf");
    }
    fwrite("1", 1, 1, fp);
    fwrite("2", 1, 1, fp);
    fwrite("3", 1, 1, fp);
    if (0 != fflush(fp)) {
        Exit("fflush");
    }
    fread(read, 1, 2, fp);
    printf("read=%s, buf=%s\n", read, buf);
    if (-1 == fclose(fp)) {
        Exit("fclose");
    }
    // 如果不加fflush, 文件中的内容和预期是不同的
    system("cat write_read.txt");

}

/*
 * 下面的代码在标准输出和重定向到文件输出的结果顺序不同, 为什么?
 * 这是因为当输出是终端时, 每次遇到\n就会刷新stdio的缓冲区, 所以内核缓冲区在之后才会接受第二句的内容.
 *
 * 如果不是终端的话, 而是文件, printf不会遇到\n刷新缓冲区, 所以内核缓冲区可能首先接收到第二句的内容.
 * */

void terminal_out() {
    printf("111\n");
    write(STDOUT_FILENO, "222\n", 4);

    FILE* fp = freopen("out.txt","w",stdout);
    if(nullptr == fp) {
        Exit("freopen");
    }
    printf("111\n");
    write(STDOUT_FILENO, "222\n", 4);
    if (0 != fclose(fp)) {
        Exit("fclose");
    }
    // 文件内容为222 111
}

int main(int argc, char* argv[]) {
    if (argc > 1 && !strcmp("-h", argv[1])) {
        printf("argv[1]=\n"
               "        0:user_buffer()\n"
               "        1:write_and_read()\n"
               "        2:terminal_out()\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):2;
    switch (type) {
        case 0:
            user_buffer();
            break;
        case 1:
            write_and_read();
            break;
        case 2:
            terminal_out();
            break;
    }
    return 0;
}