// 进程的终止

#include <unistd.h>
#include <stdlib.h>


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
 * 进程终止细节:
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
 *
 */

int main() {
    atexit
}