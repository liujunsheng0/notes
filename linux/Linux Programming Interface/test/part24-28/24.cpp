// 进程的创建

#include <unistd.h>
#include <stdio.h>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <sys/wait.h>
#include <signal.h>
#include <ostream>
#include <string>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wunused-comparison"
void exit_(const std::string &msg) {
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(errno));
    _exit(EXIT_FAILURE);
}


/* 系统调用:
 * fork()
 * exit(status)
 *      终止进程, 将系统占用的所有资源归还内核, 参数status为一整形变量, 表示进程的退出状态, 父进程可以用wait来获取该状态
 * wait(&status)
 *      1. 如果子进程尚未调用exit()终止, 那么wait()会挂起父进程直至子进程终止
 *      2. 子进程的终止状态通过wait()的status参数返回
 * execve(path(路径), argv(参数), envp(环境变量列表))
 *      加载一个新程序到当前进程的内存, 这将丢弃现存程序文本段, 并为新程序重新构建栈, 数据段, 堆.
 *
 *
 * 创建新进程, 父进程创建子进程. 子进程是父进程的翻版, 子进程获得父进程的栈, 数据段, 堆, 执行文本段的拷贝.
 * 每个进程均可修改各自的栈数据, 以及堆段中的变量, 而并不影响另一个进程.
 * pid_t fork (void)
 *      return: 父进程中: success->返回子进程ID, error->-1
 *              创建的子进程中: success->0,     error->-1
 *      notice: *完成调用后, 将存在两个进程, 且每个进程都会从fork()的返回处继续执行*
 *              fork()后, 系统率先处理哪个进程是无法确定的
 *
 * 父, 子进程间的文件共享
 *      1. 执行fork()时, 子进程会获得父进程所有文件描述符的副本, 这也意味着父子进程中的描述符均指向相同的文件句柄. 也就是说, 如果子进程更新了文件偏移量, 那么也会影响父进程中相应的描述符.
 *      2. 父子进程同时写入一文件, 共享文件偏移量会确保二者不会覆盖彼此的输出内容, 不过这并不能阻止父子进程的输出混杂在一起, 想要避免这一现象, 需要进行进程间同步
 *
 * 创建子进程后, 默认父进程先执行, 可通过将/proc/sys/kernel/sched_child_runs_first 设为非0值来改变默认值
 *
 */
void fork_() {
    printf("pid = %d fork_ start\n", getpid());
    pid_t pid = fork();
    printf("pid = %d switch\n", getpid());
    switch (pid) {
        case -1:
            exit_("fork error");
            break;
        case 0:
            printf("pid = %d child proccess fork\n", getpid());
            break;
        default:
            printf("pid = %d main  proccess fork\n", getpid());
            break;
    }
    wait(nullptr);
    printf("pid = %d fork_ end\n", getpid());
}

#define SIGSYNC SIGUSR1 // 自定义信号
void handler(int sig) {}


/*
 * 利用信号进行同步
 */
void sync_signal() {
    sigset_t block_mask,empty_mask;
    struct sigaction sa;

    setbuf(stdout,  nullptr);

    if (-1 == sigemptyset(&block_mask) || -1 == sigemptyset(&empty_mask)) {
        exit_("sigemptyset");
    }
    sigaddset(&block_mask, SIGSYNC);
    if (-1 == sigprocmask(SIG_BLOCK, &block_mask, NULL)) {
        exit_("sigprocmask");
    }

    if (-1 == sigemptyset(&sa.sa_mask)) {
        exit_("sigemptyset");
    }
    sa.sa_flags = SA_RESTART;
    sa.sa_handler = handler;
    if (-1 == sigaction(SIGSYNC, &sa, nullptr)) {
        exit_("sigaction");
    }
    switch (fork()) {
        case -1:
            exit_("fork");

        case 0: /* Child */
            /* Child does some required action here... */
            printf("[%d] Child started - doing some work\n",getpid());

            sleep(2);               /* Simulate time spent doing some work */

            // 向父进程发送信号.
            printf("[%d] Child send signal to parent [%d]\n", getpid(), getppid());
            if (kill(getppid(), SIGSYNC) == -1) {
                exit_("kill");
            }
            printf("[%d] Child finish\n",getpid());

        default: /* Parent */
            /* Parent may do some work here, and then waits for child to complete the required action */

            printf("[%d] Parent wait signal\n", getpid());
            // 等待信号到来, empty_mask将临时代替信号掩码, 执行完成后恢复
            if (sigsuspend(&empty_mask) == -1 && errno != EINTR) {
                exit_("sigsuspend");
            }
            printf("[%d] Parent got signal\n", getpid());

            /* Parent carries on to do other things... */
            printf("[%d] Parent finish\n", getpid());
    }
}

int main(int argc, char *argv[])
{
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: fork()\n"
               "0: sync_signal()\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            fork_();
            break;
        case 1:
            sync_signal();
            break;
        default:
            ;
    }
    return 0;
}