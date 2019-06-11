// 监控子进程

#include <sys/wait.h>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <cerrno>
#include <unistd.h>
#include <ostream>

void exit_(const std::string &msg) {
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(errno));
    _exit(EXIT_FAILURE);
}

/*
 * 系统调用wait等待调用进程的任一子进程终止, 参数status返回子进程的终止状态
 * pid_t wait(int *status);
 *      return process ID of child, or -1 on error(如果并无子进程, errno为ECHILD)
 * wait执行如下动作
 *      1.如果调用之前无任何子进程终止, 调用将一直阻塞, 直至某个子进程终止, 如果调用时已有子进程终止, wait立即返回
 *      2.如果status非空, 返回子进程的终止状态
 *      3.内核会为父进程下所有子进程的运行总量追加进程CPU时间以及资源使用数据
 *      4.将终止子进程的ID作为结果返回
 *
 * * wait()限制
 *      1. 无法等待指定子进程
 *      2. 无法进行非阻塞的等待
 *      3. 只能发现已经终止的子进程, 无法知道子进程的状态
 *
 * pid_t waitpid(pid_t pid, int *status, int options);
 *      return process ID of child, or -1 on error
 *      pid: >0, 等待进程ID为pid的子进程
 *           =0, 等待与调用进程统一进程组的所有子进程
 *           -1, 等待进程组标识符与pid绝对值相同的所有子进程
 *           <-1,等待任意子进程
 *      status: 掩码
 *          WNOHANG    如果pid所指定的子进程并未发生状态改变,立即返回, 不会阻塞
 *          WUNTRACED  除了返回终止子进程的信息外, 还返回因信号而终止的子进程信息
 *          WCONTINUED 返回那些因收到SIGCONT信号而恢复执行的已停止子进程的状态信息
 *          ...
 */
void wait_() {
    int times[] = {7, 1, 4};
    setbuf(stdout, NULL);  // 关闭缓冲区

    for(int i = 0; i < 3; i++) {
        switch (fork()) {
            case -1:
                exit_("fork");
            case 0: /* Child */
                printf("pid=[%d] sleep time=%d\n",getpid(), times[i]);
                sleep(times[i]);
                _exit(EXIT_SUCCESS); // **子进程退出**
            default: /* Parent */
                break;
        }
    }

    int status = 0;
    pid_t pid = 0;
    while ((pid = wait(&status)) != -1) {
        printf("pid=[%d] status=%d\n", pid, status);
    }
}


/*
 * 僵尸进程与孤儿进程
 *  孤儿进程: 进程id为1的众进程之祖-init会接管孤儿进程(父进程终止), 子进程判断父进程是否终止的方法之一是getppid()==1?
 *  僵尸进程: 父进程在执行wait()前, 子进程就已经结束. 此时系统仍然运行父进程去调用wait, 以确定子进程是如何终止的.
 *           内核通过将子进程转化为僵尸进程(zombie)来处理这种情况(释放了资源),僵尸进程保留的是内核进程表中的一条记录, 包含进程ID,终止状态等信息.(因为只是一条记录, 所以无法杀死)
 *           这样就确保了父进程总是可以调用wait()方法.
 *           当父进程执行wait后, 内核将删除僵尸进程, 如果为调用wait, init进程接管子进程并自动调用wait, 从而移除僵尸进程
 *           如果父进程创建了许多子进程,但是并未执行wait,并且进程一直运行, 势必将存在大量僵尸进程, 进而填满内核进程表, 从而妨碍了新进场的创建. 清除僵尸进程的唯一方法是杀死父进程
 *           so, 父进程应执行wait()方法, 以确保系统总是能够清理那些已经结束的进程, 避免僵尸进程
 *
 *  以下demo为展示无法杀死僵尸进程
 */
void zombie(char* path) {
    size_t buff_size = 100;
    char buff[buff_size];
    pid_t childPid;

    setbuf(stdout, NULL);       /* Disable buffering of stdout */
    printf("parent [PID=%ld]\n", (long) getpid());

    switch (childPid = fork()) {
        case -1:
            exit_("fork");
        case 0:     /* Child: immediately exits to become zombie */
            printf("child  [PID=%ld] exiting\n", (long) getpid());
            _exit(EXIT_SUCCESS);
        default:    /* Parent */
            sleep(3);               /* Give child a chance to start and exit */
            snprintf(buff, buff_size, "ps | grep %s", basename(path));
            system(buff);            /* View zombie child */

            /* Now send the "sure kill" signal to the zombie */
            if (-1 == kill(childPid, SIGKILL))
                exit_("kill");
            sleep(3);               /* Give child a chance to react to signal */
            printf("after sending SIGKILL to zombie [PID=%ld]:\n", (long) childPid);
            system(buff);            /* View zombie child again */
    }
}


int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: wait()\n"
               "1: zombie()\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            wait_();
            break;
        case 1:
            zombie(argv[0]);
            break;
    }
    return 0;
}