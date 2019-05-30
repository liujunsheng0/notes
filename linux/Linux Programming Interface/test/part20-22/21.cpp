#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <ostream>
#include <cerrno>


static int s_handle_count = 0;
static std::string s_password = "12345678";
static std::string s_key = "xxx";

void exit_(std::string msg)
{
    printf("error:%s, errno:%d, description:(%s)\n", (char*)&msg, errno, strsignal(errno));
    _exit(EXIT_FAILURE);
}

static void handler(int sig) {
    int tmp = errno;
    crypt(s_password.c_str(), s_key.c_str());
    s_handle_count++;
    errno = tmp;
}

static void handler_print(int sig) {
    printf("receive signal = %d\n", sig);
}

void sigaction_wrapper(int signal_, sighandler_t signal_handler=handler, int sa_flags=0)
{
    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = sa_flags;
    sa.sa_handler = signal_handler;
    if (sigaction(signal_, &sa, nullptr) == -1) {
        exit_("sigaction");
    }
}

/*
 * 21.1.2 可重入函数和异步信号安全函数
 * 信号处理器函数可能会在任一时间点异步中断程序的执行, 从而在同一进程中形成了两条(主程序和信号处理函数)独立的执行函数
 *
 * 可重入函数： 同一进场的多条线程可以安全地调用某一函数
 * 异步信号安全函数: 可重入, 或者信号处理函数无法将其中断的函数, 如getpid()
 *
 * 使用了malloc, free, crypt等函数是不可重入的, 因为它们使用了静态分配的内存来返回信息, 多线程调用时会相互干扰
 * (即使用了全局变量, 多线程访问时, 可能会相互干扰, 产生错误结果)
 *
 * 编写信号处理函数的选择:
 *      保证函数可重入, 且只调用异步信号安全函数
 *      当主函数执行不安全函数或是去操作信号处理函数时, 阻塞信号的传递
 *
 * 整形数据类型 sig_atomic_t, 意在保证读写操作的原子性, 因此所有子啊主程序与信号处理函数之间共享的全局变量都应声明如下:
 *      volatile sig_atomic_t v;
 *
 * crypt函数, 可重入测试
 *
 */
void reentrant() {   // reentrant: 可重入
    char *crypt_result;

    crypt_result = strdup(crypt(s_password.c_str(), s_key.c_str()));
    if (crypt_result == nullptr) {
        exit_("strdup");
    }

    sigaction_wrapper(SIGINT);

    for (int call_num = 0, mismatch = 0; mismatch < 10; call_num++) {
        /* Ctrl + C 产生信号, 如果是可重入的, 加密结果是一样的
         * 在不产生信号的情况下, 加密结果总是相同的, 然而, 一旦收到SIGINT信号, 而主程序又恰好在for循环的crypt()调用之后,
         * 字符串的匹配检查之前遭到信号处理函数的中断, 此时就发生了字符串不匹配的情况
         */
        if (strcmp(crypt(s_password.c_str(), s_key.c_str()), crypt_result) != 0) {
            mismatch++;
            printf("mismatch on call %d (mismatch=%d handled=%d)\n", call_num, mismatch, s_handle_count);
        }
    }
}

/*
 * 终止信号处理函数的方法
 *     1. 信号的默认动作是终止进程, 如Ctrl + C
 *     2. 信号处理函数中执行非本地跳转
 *        例如, 一旦收到SIGINT信号(Ctrl+C), shell执行一个非本地跳转, 将控制权返回到主输入循环中(循环执行系统调用), 以便读取下一条指令
 *             for循环中执行sleep(), 按Ctrl+C就会中断sleep
 *     3. 使用abort()函数终止进程, 并产生核心转储
 *
 * 系统调用的中断和重启
 * 设置标志SA_RESTART可以达到自动重启被中断的系统调用, 但是并非所有的系统调用都可以制定SA_RESTART来达到自动重启的目的.(部分历史原因)
 *      4.2BSD引入了重启系统调用的概念. I/O的系统调用都是可中断的,所以只有在操作慢速设备时, 才可以利用SA_RESTART来自动重启系统调用;
 *      (慢速设备包括终端, 管道, FIFO, 套接字(socket))
 *      (系统调用被中断时, errno=EINTR(中断操作)
)
 *      可以自动重启的系统调用:
 *          1. 等待子进程: wait(), waitpid(), wait3()...
 *          2. I/O: read(), readv(), write(), writev()
 *          3. 系统调用open()
 *          4. 套接字的系统调用: accept(), accept4(), connect(), send(), recv()....
 *          5. 对POSIX消息队列进行I/O操作的系统调用: mq_receive(), mq_send()...
 *          6. 用于设置文件锁: flock(), fcntl()
 *          7. 用于同步POSIX线程的函数: pthread_mutex_lock(), phread_mutex_trylock()...
 *          ....
 *
 *       绝对不会重启的系统调用:
 *          1. poll(), ppoll(), select(), pselect()多路复用调用
 *          2. epoll_wait(), io_getevents()...
 *          3. 对inotify文件描述符发起的read调用
 *          4. 讲进程挂起的系统调用sleep(), nanosleep(), clock_nanosleep().
 *          5. 等待信号的系统调用: pause(), sigsuspend(), ssigwaitinfo()....
 *
 */
void interrupted() { // interrupted:中断
#define BUFSIZE 100
    char buf[BUFSIZE];

    // 直接中断read
    sigaction_wrapper(SIGINT);
    for (int i = 1; i < 5; i++) {
        memset(buf, 0, 100);
        read(STDIN_FILENO, buf, BUFSIZE);
        if (errno == EINTR) {
            printf("times1 = %d, read interrupted\n", i);
        } else {
            printf("times1 = %d, input = %s\n", i, buf);
        }
    }

    errno = 0;
    // 中断系统调用read后重启
    sigaction_wrapper(SIGINT, handler_print, SA_RESTART);
    for (int i = 1; i < 5; i++) {
        memset(buf, 0, 100);
        read(STDIN_FILENO, buf, BUFSIZE);
        if (errno == EINTR) {
            printf("times2 = %d, read interrupted\n", i);
        } else {
            printf("times2 = %d, input = %s\n", i, buf);
        }
    }
}

// g++ 21.cpp  -lcrypt
int main(int argc, char *argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: reentrant\n"
               "1: interrupted\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 1:
            interrupted();
            break;
        default:
            reentrant();
    }
    return 0;
}