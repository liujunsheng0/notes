#define _BSD_SOURCE
#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void                    /* Print list of signals within a signal set */
printSigset(const char *prefix, const sigset_t *sigset)
{
    int sig, cnt;

    cnt = 0;
    for (sig = 1; sig < NSIG; sig++) {
        if (sigismember(sigset, sig)) {
            cnt++;
            printf("prefix=%s sig=%d description=(%s)\n", prefix, sig, strsignal(sig));
        }
    }

    if (cnt == 0)
        printf("prefix=%s <empty signal set>\n", prefix);
}
int                     /* Print mask of blocked signals for this process */
printSigMask(const char *msg)
{
    sigset_t currMask;

    if (msg != NULL)
        printf("%s", msg);

    if (sigprocmask(SIG_BLOCK, NULL, &currMask) == -1)
        return -1;

    printSigset("\t\t", &currMask);

    return 0;
}
int                     /* Print signals currently pending for this process */
printPendingSigs(const char *msg)
{
    sigset_t pendingSigs;

    if (msg != NULL)
        printf("%s\n", msg);

    if (sigpending(&pendingSigs) == -1)
        return -1;

    printSigset("pending", &pendingSigs);

    return 0;
}

void sig_handler(int sig) {
    printf("new signal handler sig = %d\n", sig);              /* Unsafe */
}

void test_signal() {
    // 重设置了SIGINT的信号处理函数, 收到此信号时, 调用
    // SIGINT:终端输入Control + C时, 终端产生此信号
    void (*old_handler)(int);
    old_handler = signal(SIGINT, sig_handler);
    if(old_handler == SIG_ERR) {
        printf("error\n");
        return;
    }
    sleep(5);
}

void test_signal_handler() {
    // 重设置了SIGINT的信号处理函数, 收到此信号时, 调用
    // SIGINT:终端输入Control + C时, 终端产生此信号
    void (*old_handler)(int);
    old_handler = signal(SIGINT, sig_handler);
    if(old_handler == SIG_ERR) {
        printf("error\n");
        return;
    }
    int times = 10;
    for(int j = 0; j < times; j++) {
        printf("j = %d\n", j);
        sleep(5);  // 输入Control + C时, 终止了sleep
    }
    // 将SIGINT信号处理器回复为默认处理器
    printf("SIGINT TO DEFAULT");
    if (signal(SIGINT, old_handler) == SIG_ERR){
        printf("error\n");
    }
}


void test_raise() {
    if(signal(SIGINT, sig_handler) == SIG_ERR) {
        printf("error\n");
        return;
    }
    for(int i = 0; i < 10; i++) {
        if (raise(SIGINT) == -1) {
            printf("raise error %d\n", i);
        } else {
            printf("raise success %d\n", i);
        }
    }
    sleep(1);
}

void test_sigset_t() {
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        printf("sigemptyset error\n");
    }
    printSigset("empty", &sigs);
    printf("sigisemptyset: %d\n", sigisemptyset(&sigs));
    printf("sigismember: SIGINT %d\n", sigismember(&sigs, SIGINT));
    if (sigaddset(&sigs, SIGINT) == -1) {
        printf("sigaddset error\n");
    }
    printf("sigismember: SIGINT %d\n", sigismember(&sigs, SIGINT));

    if (sigfillset(&sigs) == -1) {
        printf("sigfillset error\n");
    }
    printSigset("fill", &sigs);
    printf("sigisempty: %d\n", sigisemptyset(&sigs));
    printf("sigismember: SIGINT %d\n", sigismember(&sigs, SIGINT));
    if (sigdelset(&sigs, SIGINT) == -1) {
        printf("sigdelset error\n");
    }
    printf("sigismember: SIGINT %d\n", sigismember(&sigs, SIGINT));
}

void test_mask() {
    if(signal(SIGINT, sig_handler) == SIG_ERR) {
        printf("signal error\n");
    }
    if(signal(SIGTSTP, sig_handler) == SIG_ERR) {
        printf("signal error\n");
    }
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        printf("sigemptyset error\n");
    }
    // SIGTSTP ctrl + Z
    if (sigaddset(&sigs, SIGINT) == -1 || sigaddset(&sigs, SIGTSTP)) {
        printf("sigaddset error\n");
    }
    // SIGTSTP 和 SIGINT添加置掩码
    if (sigprocmask(SIG_BLOCK, &sigs, NULL) == -1) {
        printf("sigprocmask error");
    }
    if(raise(SIGTSTP) == -1 || raise(SIGINT) == -1) {
        printf("raise error");
    }
    printPendingSigs("mask1");
    // SIGTSTP 和 SIGINT从掩码中移除
    if (sigprocmask(SIG_UNBLOCK, &sigs, NULL) == -1) {
        printf("sigprocmask error");
    }
    printPendingSigs("mask2");
}

void test_signal_queue() {
    sigset_t sigs;
    if (sigemptyset(&sigs) == -1) {
        printf("sigemptyset error\n");
    }
    // SIGTSTP ctrl + Z
    if (sigaddset(&sigs, SIGINT) == -1 || sigaddset(&sigs, SIGTSTP)) {
        printf("sigaddset error\n");
    }
    // SIGTSTP 和 SIGINT添加置掩码
    if (sigprocmask(SIG_BLOCK, &sigs, NULL) == -1) {
        printf("sigprocmask error");
    }
    for (int i = 0; i < 100; i++) {
        if(raise(SIGTSTP) == -1 || raise(SIGINT) == -1) {
            printf("raise error");
        }
    }
    printPendingSigs("queue");
}


void test_pause() {
    pause();
}

int main(int argc, char *argv[]) {
//    test_signal();
//    test_signal_handler();
    test_sigset_t();
    test_signal_queue();
    return 0;
}