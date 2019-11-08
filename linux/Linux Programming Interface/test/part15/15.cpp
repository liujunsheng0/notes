#include <sys/stat.h>
#include <stdio.h>
#include <utime.h>

#include "error_functions.h"

/*
 * 文件的各种属性(文件元数据)
 * 获取与文件有关信息的系统调用, stat(), lstat(), fstat()
 * int stat (const char *pathname, struct stat *statbuf);
 *      return 0 on success; -1 on error
 *      返回命名文件的相关信息
 * int lstat(const char *pathname, struct stat *statbuf);
 *      return 0 on success; -1 on error
 *      与stat()类似, 区别在与如果文件属于符号链接, 那么所返回的信息针对的是符号链接自身, 而非链接文件
 * int fstat(int fd, struct stat *statbuf);
 *      return 0 on success; -1 on error
 *      返回由某个打开文件描述符所指代文件的相关信息
 *  struct stat {
 *      dev_t   st_dev;   文件所驻留的设备, 记录了设置的主, 辅ID
 *      ino_t   st_ino;   包含了文件的i-node number, 由st_dev和st_ino可确认文件
 *      mode_t  st_mode;  内含位掩码, 起标识文件类型和指定文件权限的双重作用
 *                        与常量S_IFMT相与, 可获取文件类型
 *                        低十二位定义了文件权限, 其中低9位分别表示文件属主, 数组, 其他用户的读写执行权限
 *      nlink_t st_nlink; 硬链接数
 *      uid_t   st_uid;   用户ID
 *      gid_t   st_gid;   组ID
 *      dev_t   st_rdev;
 *      off_t   st_size;  文件的字节数, 对于符号链接, 则表示链接所指路径名的长度
 *      blksize_t st_blksize; 非底层文件系统的块大小
 *      blkcnt_t st_blocks;   分配给文件的总块数, 包括了为指针块所分配的块, 一般来说块大小为512字节
 *      time_t st_atime;   Time of last file access, 上次访问时间
 *      time_t st_mtime;   Time of last file modify, 上次修改时间
 *      time_t st_ctime;   Time of last status change
 *                         文件状态发生改变的时间, 即i-node发生变化的时间
 *                         时间均为时间戳, 距1970.1.1所经历的的秒数
 *  };
 *
 *  各种函数对文件时间戳的影响
 *            文件/目录         父目录
 *          a     m     c     a     m     c
 *  chmod               1
 *  chown               1
 *  link                1           1     1
 *
 */
void stat_test() {
    struct stat statbuf;
    if (stat("../data/test.txt", &statbuf) == -1) {
        Exit("stat error");
    }
    printf("st_dev  =%d\n", statbuf.st_dev);
    printf("st_ino  =%d\n", statbuf.st_ino);
    switch (statbuf.st_mode & S_IFMT) {
        case S_IFREG:  printf("regular file\n");            break;
        case S_IFDIR:  printf("directory\n");               break;
        case S_IFCHR:  printf("character device\n");        break;
        case S_IFBLK:  printf("block device\n");            break;
//        case S_IFLNK:  printf("symbolic (soft) link\n");    break;
        case S_IFIFO:  printf("FIFO or pipe\n");            break;
//        case S_IFSOCK: printf("socket\n");                  break;
        default:       printf("unknown file type?\n");      break;
    }
    printf("st_nlink=%d\n", statbuf.st_nlink);
    printf("st_uid  =%d\n", statbuf.st_uid);
    printf("st_gid  =%d\n", statbuf.st_gid);
    printf("st_rdev =%d\n", statbuf.st_rdev);
    printf("st_size =%ld\n", statbuf.st_size);
    printf("st_atime=%d\n", statbuf.st_atime);
    printf("st_mtime=%d\n", statbuf.st_mtime);
    printf("st_ctime=%d\n", statbuf.st_ctime);
}

/*
 * #include <utime.h>
 * int utime(const char *pathname, const struct utimbuf *buf);
 *      return 0 on success; -1 on error
 *      如果buf为NULL, 将文件的上次访问和修改时间同时置为当前时间
 * struct utimbuf {
 *      time_t actime;  上一次访问时间
 *      time_t modtime; 上一次修改时间
 * };
 * #include <sys/time.h>
 * int utimes(const char *pathname, const struct timeval tv[2]);
 *      return 0 on success; -1 on error
 *      作用与utime()相同, 提供了纳秒级精度的支持
 */

void utime_test() {
    struct utimbuf ut;
    ut.actime = 1000000000;
    ut.modtime = 2000000000;
    struct stat st;
    const char *path = (char *) "../data/test.txt";
    if (-1 == stat(path, &st)) {
        Exit("stat error");
    }
    printf("st_atime=%d, st_mtime=%d\n", st.st_atime, st.st_mtime);
    if (-1 == utime(path, NULL)) {
        Exit("utime error");
    }
    if (-1 == stat(path, &st)) {
        Exit("stat error");
    }

    printf("st_atime=%d, st_mtime=%d\n", st.st_atime, st.st_mtime);
    if (-1 == utime(path, &ut)) {
        Exit("utime error");
    }
    if (-1 == stat(path, &st)) {
        Exit("stat error");
    }
    printf("st_atime=%d, st_mtime=%d\n", st.st_atime, st.st_mtime);
}

/*
 * 文件权限
 *      stat 结构中st_mode的低十二位定义了文件权限, 前三位分布是set-user-ID, set-group-ID, sticky(U, G, T)
 *      文件权限分为三类:
 *          Owner(user): 文件属主的权限
 *          Group:       文件属组成员用户的权限
 *          Other:       授予其他用户的权限
 *      每类用户授予的权限
 *          Read:   读文件的内容
 *          Write:  更改文件的内容
 *          Execute:可以执行文件. 要执行脚本文件, 需要同时具备读和执行权限
 * 目录权限
 *      Read:    可列出目录之下的文件名
 *      Write:   可在目录内创建, 删除文件. 要删除文件时, 对文件本身无需有任何权限.
 *      Execute: 可访问目录中的文件, 有时也将对目录的执行权限称为搜索权限
 *      1. 拥有对目录的读权限, 用户只能查看目录中的文件列表, 想要访问目录内文件的内容或是这些文件的i节点信息, 需要拥有对
 *         目录的执行权限
 *      2. 如果仅拥有对目录的可执行权限, 而无读权限, 只要知道目录内文件的名称, 扔可对其访问, 但是不能列出目录下的内容
 *      3. 要想在目录中添加/删除文件, 需要同时拥有对该目录的执行和写权限
 *      4. 访问权限时, 需要拥有对路径名中所有目录拥有执行权限,
 *         a. 如想要读取/home/test/test.txt，则需要拥有对目录/, /home, /home/test的执行权限
 *         b. 假设当前工作目录为/home/test/sub1, 访问../sub2/test.txt, 则需要拥有对/home/test和/home/test/sub2的可执行
 *            权限, 不必有对/或/home的执行权限
 * 权限检查算法
 *      只要在访问文件/目录的系统调用中指定了路径名称, 内核就会检查响相应文件的权限, 如果赋予系统调用的路径名包含了目录
 *      前缀时, 那么内核不仅会检查对文件本身所需要的权限，还会检查前缀每个目录的可执行权限.
 *      内核会使用进程的有效用户ID, 有效组ID以及辅助组ID来执行权限检查
 *      一旦成功打开文件后, 针对返回描述符的系统调用将不再进行任何权限检查
 *
 */


int main() {
//    stat_test();
    utime_test();
    return 0;
}