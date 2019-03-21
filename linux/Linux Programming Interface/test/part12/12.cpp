/*
 * /proc 虚拟文件系统
 *      各种系统信息
 *      包含了各种用于展示内核信息的文件,并且允许进程通过常规文件I/O系统调用读取.
 *      其包含的文件和子目录并未存储于磁盘上, 而是由内核动态生成
 *
 * /proc/PID
 *      系统中的每个进程, 内核都提供了相应的目录, 命名为/proc/PID, PID是进程ID
 *      cmdline 以\0分隔的命令行参数
 *      cwd     指向当前工作目录的符号链接
 *      environ NAME=value 环境变量, 以\0分隔
 *      exe     指向正在执行文件的符号链接
 *      fd      文件目录, 包含了由进程打开文件的符号链接, 文件描述符->文件的符号链接
 *      maps    内存映射
 *      mem     进程虚拟内存
 *      mounts  进程的安装点
 *      root    指向根目录的符号链接
 *      status  各种信息, 如进程ID, 凭证, 内存使用量, 信号等
 *      task    进程中的每个线程均包含一个子目录
 *          task/TID命名的子目录, TID是线程ID
 *      version  系统相关信息
 *      为方便起见, 任何进程都可使用符号链接/proc/self来访问自己的/proc/PID目录
 *
 * /proc/net          有关网络和套接字的状态信息
 * /proc/sys/fs       文件系统相关配置, fs = file system
 * /proc/sys/kernel   各种常规的内核配置
 * /proc/sys/net      网络和套接字的设置
 *
 *
 * 系统标识: 系统调用uname()
 *      命令uname -a 返回系统相关信息
 *
 */

#ifdef __linux__
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <sys/utsname.h>
#include "error_functions.h"

void uname_a() {
    struct utsname uts;

    if (uname(&uts) == -1)
        errExit("uname");

    printf("Node name:   %s\n", uts.nodename);
    printf("System name: %s\n", uts.sysname);
    printf("Release:     %s\n", uts.release);
    printf("Version:     %s\n", uts.version);
    printf("Machine:     %s\n", uts.machine);
    #ifdef _GNU_SOURCE
    printf("Domain name: %s\n", uts.domainname);
    #endif
}

int main(int argc, char *argv[])
{

    return 0;
}