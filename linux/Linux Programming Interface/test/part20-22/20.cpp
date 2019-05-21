#define _BSD_SOURCE
#include <csignal>
#include <cstdio>
#include <cstring>
#include <unistd.h>
#include <cerrno>
#include <cstdlib>
#include <string>

void exit_(std::string msg)
{
    printf("error:%s, errno:%d, description:(%s)\n", (char*)&msg, errno, strsignal(errno));
    _exit(EXIT_FAILURE);
}

/* 打印信号集合中包含信号 */
void print_signal_set(const char *prefix, const sigset_t *sigset)
{
    bool empty = true;
    for (int sig = 1; sig < NSIG; sig++) {
        if (sigismember(sigset, sig)) {
            empty = false;
            printf("prefix=%s  sig=%-2d  description=(%s)\n", prefix, sig, strsignal(sig));
        }
    }
    if (empty) {
        printf("prefix=%s <empty signal set>\n", prefix);
    }
}

/* 打印进程阻塞的信号 */
int print_signal_mask(const char *msg)
{
    sigset_t mask;
    if (msg != NULL) {
        printf("%s", msg);
    }

    // 获取阻塞的信号
    if (sigprocmask(SIG_BLOCK, NULL, &mask) == -1) {
        return -1;
    }

    print_signal_set("\t\t\t", &mask);

    return 0;
}

/* 打印当前进程中处于pending状态的信号 */
int print_pending_signal(const char *msg)
{
    sigset_t pending_signal;

    if (msg != NULL) {
        printf("%s\n", msg);
    }

    if (sigpending(&pending_signal) == -1) {
        return -1;
    }

    print_signal_set("pending", &pending_signal);

    return 0;
}

void new_signal_handler(int sig)
{
    printf("new signal handler:: signal = %d, description = %s\n",
            sig, strsignal(sig)); /* Unsafe */
}

// signal()的再次封装
// Set the handler for the signal SIG to signal_handler,
// returning the old handler, or SIG_ERR on error.
//void (*signal_wrapper(int signal_, void(*signal_handler)(int))) (int) 与下述定义等价
sighandler_t signal_wrapper(int signal_, sighandler_t signal_handler)
{
    // void (*old_handler)(int); 等价定义
    sighandler_t old_handler;
    old_handler = signal(signal_, signal_handler);
    if(old_handler == SIG_ERR) {
        exit_("signal_wrapper error");
    }
    return old_handler;
}

// 重写SIGINT的信号处理函数
void test_signal()
{
    int seconds = 3;
    // SIGINT:终端输入Control + C时, 终端产生此信号
    void (*old_handler)(int);

    printf("set SIGINT to new signal handler\n");
    old_handler = signal_wrapper(SIGINT, new_signal_handler);
    int times = 5;
    for(int j = 0; j < times; j++) {
        sleep(seconds);  // 输入Control + C时, 终止了sleep(信号中断)
    }
    // 将SIGINT信号处理器回复为默认处理器
    printf("set SIGINT handler to default\n");
    signal_wrapper(SIGINT, old_handler);
    // 此时输入control + c直接退出程序
    sleep(seconds);
    printf("test_signal finish\n");
}

// 测试raise函数, 向进程本身发送信号
void test_raise()
{
    printf("set SIGINT to new signal handler\n");
    signal_wrapper(SIGINT, new_signal_handler);
    printf("start raise SIGINT...\n");
    for(int i = 0; i < 3; i++) {
        printf("\traise SIGINT %s\n", -1 == raise(SIGINT) ? "error": "success") ;
    }
    sleep(1);
}

// 测试struct sigset_t
void test_sigset_t()
{
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        exit_("sigemptyset error");
    }
    printf("sigset is empty ?    %d\n", sigisemptyset(&sigs));
    printf("SIGINT in sigset?    %d\n", sigismember(&sigs, SIGINT));
    printf("add SIGINT to sigset\n");
    if (sigaddset(&sigs, SIGINT) == -1) {
        exit_("sigaddset error");
    }
    printf("SIGINT in sigset?    %d\n", sigismember(&sigs, SIGINT));
    printf("Set all signals in sigset\n");
    if (sigfillset(&sigs) == -1) {
        exit_("sigfillset error");
    }
    print_signal_set("all signals", &sigs);
    printf("sigset is empty ?    %d\n", sigisemptyset(&sigs));
    printf("SIGINT in sigset?    %d\n", sigismember(&sigs, SIGINT));
    printf("remove SIGINT from sigset\n");
    if (sigdelset(&sigs, SIGINT) == -1) {
        exit_("sigdelset error");
    }
    printf("SIGINT in sigset?    %d\n", sigismember(&sigs, SIGINT));
}

// 信号掩码的新增和移除
void test_mask() {
    // SIGTSTP = Control + z
    signal_wrapper(SIGINT, new_signal_handler);
    signal_wrapper(SIGTSTP, new_signal_handler);
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        exit_("sigemptyset error");
    }
    printf("add SIGINT,SIGTSTP(ctrl+c,z) to mask\n");
    // SIGTSTP ctrl + Z
    if (sigaddset(&sigs, SIGINT) == -1 || sigaddset(&sigs, SIGTSTP) == -1) {
        exit_("sigaddset error");
    }
    // SIGTSTP 和 SIGINT添加置掩码
    if (sigprocmask(SIG_BLOCK, &sigs, NULL) == -1) {
        exit_("sigprocmask error");
    }
    if(raise(SIGTSTP) == -1 || raise(SIGINT) == -1) {
        exit_("raise error");
    }
    print_pending_signal("mask is not empty");

    printf("remove SIGINT,SIGTSTP(ctrl+c,z) from mask\n");
    // SIGTSTP 和 SIGINT从掩码中移除
    if (sigprocmask(SIG_UNBLOCK, &sigs, NULL) == -1) {
        exit_("sigprocmask error");
    }
    print_pending_signal("mask is empty");
}

// pending signal
void test_signal_pending() {
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        exit_("sigemptyset error");
    }
    // SIGTSTP = ctrl + Z
    if (sigaddset(&sigs, SIGINT) == -1 || sigaddset(&sigs, SIGTSTP)) {
        exit_("sigaddset error");
    }
    printf("add SIGINT,SIGTSTP(ctrl+c,z) to mask\n");
    if (sigprocmask(SIG_BLOCK, &sigs, NULL) == -1) {
        exit_("sigprocmask error");
    }

    printf("raise 100*(SIGINT,SIGTSTP) to process\n");
    for (int i = 0; i < 100; i++) {
        if(raise(SIGTSTP) == -1 || raise(SIGINT) == -1) {
            exit_("raise error");
        }
    }
    print_pending_signal("pending signal");
}

int main(int argc, char *argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: test_signal\n"
               "1: test_raise\n"
               "2: test_sigset_t\n"
               "3: test_mask\n"
               "4: test_signal_pending\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;

    printf("type = %d\n", type);
    switch (type) {
        case 0:
            test_signal();
            break;
        case 1:
            test_raise();
            break;
        case 2:
            test_sigset_t();
            break;
        case 3:
            test_mask();
            break;
        case 4:
            test_signal_pending();
            break;
        default:
            ;
    }
    return 0;
}