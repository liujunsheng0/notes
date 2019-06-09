// 进程的终止

#include <unistd.h>
#include <stdlib.h>
#include <cstdio>
#include <cstring>
#include <cerrno>
#include <iostream>

void exit_(char *msg) {
    printf("error %s, errno=%d, %s\n", msg, errno, strerror(errno));
    exit(EXIT_FAILURE);
}

/*
 * void _exit(int status);
 *      status: 进程的终止状态, 父进程可用wait()获取该状态, 但是仅低8位可为父进程所用
 *              0: 表示进程功成身退, 非0:表示进程因异常退出
 *      通用常量   EXIT_SUCCESS(0)  EXIT_FAILURE(非0)
 *
 * void exit(int status) {
 *      while(_exit_funcs != NULL) {
 *          ...
 *          _exit_funcs = _exit_funcs->next;
 *      }
 *      ...
 *      flush_cache();
 *      _exit(status);
 *  }
 *  其中_exit_funcs是存储由atexit()和on_exit()注册的函数的链表, 而这个while循环则遍历该链表并逐个调用这些注册的函数(调用顺序与注册顺序相反).
 *  so ,exit()和_exit()的区别在于,
 *      1. exit()会首先将所有注册的函数进行调用以后再退出,而_exit()则是直接结束程序
 *      2. exit()会刷新stdio流缓冲区
 *
 *  main()函数中返回, 执行return n等同于exit(n), 因为调用main()的运行函数时会将main()的返回值作为exit()的参数
 *
 * 进程终止细节:(不管进程正常终止与否, 内核都会执行多个清理步骤)
 *  1. 关闭所有打开文件描述符, 目录流, 信息目录描述符, 转换描述符
 *  2. 关闭文件描述符关闭的后果之一, 释放该进程所持有的任何文件锁
 *  3. 分离任何已连接的System V共享内存段
 *  4. 关闭信号量, 取消内存映射, 关闭POSIX消息队列
 *  5. ...
 *
 *  注册退出处理函数
 *  int atexit(void (*func)(void));
 *      return: 0 on success, 非0 on error
 *      usage:  将func加到一个函数列表中, 进程终止时调用列表中的函数, 调用顺序与注册顺序相反;
 *      notice: 一旦有任一退出处理函数无法返回(调用_exit, 信号终止, 函数异常...), 那么将不会再调用剩余的处理函数, 此外调用exit()
 *              时需要执行的剩余动作也将不会在执行.
 *      缺点:   1. 退出处理函数时, 无法得知传递给exit()的状态
 *             2. 无法给退出处理函数指定参数
 *  为了摆脱atexit()的限制, 可使用on_exit(), 但是避免使用, 因为大部分UNIX并不支持这一系统调用
 *  int on_exit(void (*__func) (int status, void *arg), void *arg)
 *      return: 0 on success, 非0 on error
 *      arg:    传递给退出处理函数的参数拷贝
 *      notice: 与atexit的退出处理函数在同一调用链上.
 */
void atexit_() { printf("atexit\n"); }
void on_exit_(int status, void* n) {
    printf("on exit, status=%d, arg=%ld\n", status, (long)n);
}

/*
 * fork() stdio缓冲区以及_exit()的交互
 * 执行g++ 25.cpp && ./a.out 1
 *      输出:  hello world
 *            write to STDOUT_FILENO
 * 执行g++ 25.cpp && ./a.out 1 > a && cat a
 *      输出:  write to STDOUT_FILENO
 *            hello world
 *            hello world
 *  原因: write会直接将数据传递给内核缓冲区, fork不会复制这一缓冲区.
 *       进程在用户空间内存中维护stdio缓冲区的, 所以fork时会复制这些缓冲区.
 *       当标准输出到终端时,
 *          默认为行缓冲, 所以立即显示printf输出的字符串
 *       当标准输出到文件时,
 *          默认为块缓冲, 当调用fork时, printf的字符串仍在父进程的stdio缓冲区中, 并随子进程的创建而产生了副本,
 *          父子进程在调用exit()时会刷新各自的stdio缓冲区, 从而导致了重复的输出结果.
 *       当定向到文件时, write的输出结果先于printf, 因为write会立即传递给内核高速缓冲区, 而printf的结果需要等到调用exit()刷新stdio缓冲区
 *  避免方法:
 *      在调用fork()前, 使用fflush()刷新缓冲stdio缓冲区, 或者使用setbuf()来stdio流的缓冲功能
 *      子进程使用_exit(), 以便不刷新缓冲区
 *  通用原则:
 *      在创建子进程的应用中, 应该仅有一个进程(一般为父进程)通过调用exit()终止, 而其他进程应调用_exit()终止,
 *      从而确保了只有一个进程调用退出处理函数, 并刷新stdio缓冲区.
 */
void exit_interactive() {
    printf("hello world pid=%d\n", getpid());
    write(STDOUT_FILENO, "write to STDOUT_FILENO\n", 24);
    if (-1 == fork()){
        exit_((char *)("fork error"));
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: atexit()\n"
               "1: exit_interactive()\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            if (0 != atexit(atexit_) || 0 != atexit(atexit_) || on_exit(on_exit_, (void*) 10)) {
                exit_((char*)"atexit register error\n");
            }
            break;
        case 1:
            exit_interactive();
            break;
        default:
            ;
    }
    return 0;
}