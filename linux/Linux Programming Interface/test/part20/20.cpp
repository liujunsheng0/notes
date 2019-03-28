#define _BSD_SOURCE
#include <signal.h>
#include <stdio.h>
#include <unistd.h>



static void sig_handler(int sig) {
    printf("Ouch!\n");              /* Unsafe */
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


int main(int argc, char *argv[]) {
    test_signal_handler();
    return 0;
}