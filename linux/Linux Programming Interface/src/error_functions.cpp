//
// Created by ljs on 19-3-2.
//

#include <stdarg.h>
#include "../include/error_functions.h"
#include "../include/header.h"

#ifdef __GNUC__
__attribute__ (( __noreturn__ ))
#endif

/*
void exit(int status) {
    while(_exit_funcs != NULL)
    {
        ...
        _exit_funcs = _exit_funcs->next;
    }
    ...
    _exit(status);
}
    其中_exit_funcs是存储由__cxa_atexit和atexit注册的函数的链表,而这个while循环则遍历该链表并逐个调用这些注册的函数.
    最后再调用_exit(),这个函数的作用仅仅是调用了exit这个系统调用.即_exit()调用后,进程会直接结束.

    so ,exit()和_exit()的区别在于, exit()会首先将所有使用atexit注册的函数进行调用以后再退出,而_exit()则是直接结束程序
 */
static void terminate(Boolean useExit) {
    char *s;
    s = getenv("EF_DUMPCORE");
    if (s != NULL && *s != '\0') {
        abort();
    } else if (useExit) {
        exit(EXIT_FAILURE);
    } else {
        _exit(EXIT_FAILURE);
    }
}


/*
 * vsnprintf  参数数量不固定时使用
 * snprintf   参数数量固定时使用, 函数原型为int snprintf(char *str, size_t size, const char *format, ...).
 * 将可变参数 “…” 按照format的格式格式化为字符串, 然后再将其拷贝至str中.
 * va_list变量. va:variable-argument:可变参数
 */
static void outputError(Boolean useErrnoMsg, int err, Boolean flushStdout, const char* format, va_list ap) {
#define BUFSIZE 500
    char buf[BUFSIZE], userMsg[BUFSIZE], errText[BUFSIZE];
    vsnprintf(userMsg, BUFSIZE, format, ap); // 将可变参数格式化输出到一个字符数组.
    if (useErrnoMsg) {
        snprintf(errText, BUFSIZE, "[%s]", strerror(err));
    }

    snprintf(buf, BUFSIZE, "ERROR %s %s", errText, userMsg);

    if (flushStdout) {
        fflush(stdout);
    }

    fputs(buf, stderr);
    fflush(stderr);
}


/*
 * 栈是从高地址向低地址生长的. 堆是从低地址向高地址生长的
 * va_start 读取可变参数的过程其实就是在堆栈中, 使用指针,遍历堆栈段中的参数列表,从低地址到高地址一个一个地把参数内容读出来的过程·
 * 函数参数是以数据结构:栈的形式存取,从右至左入栈.
 * 首先是参数的内存存放格式：参数存放在内存的堆栈段中,在执行函数的时候,从最后一个开始入栈.因此栈底高地址,栈顶低地址,举个例子如下：
 * void func(int x, float y, char z);
 * 那么,调用函数的时候,实参 char z 先进栈,然后是 float y,最后是 int x,因此在内存中变量的存放次序是 x->y->z,
 * 因此,从理论上说,我们只要探测到任意一个变量的地址,并且知道其他变量的类型,通过指针移位运算,则总可以顺藤摸瓜找到其他的输入变量.
 *
 * 获取所有的参数之后,我们有必要将这个 va_list实例args指针关掉,以免发生危险,方法是调用 va_end,将args置为NULL,
 * 应该养成获取完参数表之后关闭指针的习惯. 说白了,就是让程序具有健壮性.通常va_start和va_end是成对出现
 */

void Exit(const char *format, ...) {
    va_list args;
    va_start(args, format);
    outputError(TRUE, errno, TRUE, format, args);
    va_end(args);
    terminate(TRUE);

}