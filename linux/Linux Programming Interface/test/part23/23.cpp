#define _POSIX_C_SOURCE 199309
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <pthread.h>
#include <stdio.h>
#include <cstring>

/*
 * 定时器与休眠
 *
 * errno == EINTR 时, 说明中断了系统调用
 * 收到此信号SIGALRM时, 定时器到期发出的信号
 */


static volatile sig_atomic_t s_get_alarm = 0;

void exit_(char *msg) {
    printf("error %s, errno=%d, %s\n", msg, errno, strerror(errno));
    _exit(EXIT_FAILURE);
}

void signal_handler1(int sig)
{
    s_get_alarm = 1;
}

void signal_handler2(int sig)
{
    printf("catch signal\n");          /* UNSAFE (see Section 21.1.2) */
    fflush(stdout);
}

void mysigaction(int sig, void (*sig_handler)(int), bool is_restart=false) {
    struct sigaction sa;

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (is_restart) {
        sa.sa_flags = SA_RESTART;
    }
    sa.sa_handler = sig_handler;
    if (sigaction(sig, &sa, NULL) == -1) {
        exit_("sigaction");
    }
}

struct itimerval create_itimerval(int iv_s=5, int iv_us=0, int ii_s=5, int ii_us=0) {
    struct itimerval itv;
    itv.it_value.tv_sec = iv_s;
    itv.it_value.tv_usec = iv_us;
    itv.it_interval.tv_sec = ii_s;
    itv.it_interval.tv_usec = ii_us;
    return itv;
}


void display_time(const char *msg, bool includeTimer)
{
    struct itimerval itv;
    static struct timeval start;
    struct timeval curr;
    static int callNum = 0;             /* Number of calls to this function */

    if (callNum == 0 && -1 == gettimeofday(&start, NULL)) {
        exit_("gettimeofday");
    }

    if (callNum % 10 == 0) {
        printf("       Elapsed   It Value  Interval\n");
    }

    if (gettimeofday(&curr, NULL) == -1) {
        exit_("gettimeofday");
    }
    printf("%-7s %6.2f", msg, curr.tv_sec - start.tv_sec + (curr.tv_usec - start.tv_usec) / 1000000.0);

    if (includeTimer) {
        if (getitimer(ITIMER_REAL, &itv) == -1) {
            exit_("getitimer");
        }
        printf("  %6.2f  %6.2f",
               itv.it_value.tv_sec + itv.it_value.tv_usec / 1000000.0,
               itv.it_interval.tv_sec + itv.it_interval.tv_usec / 1000000.0);
    }

    printf("\n");
    callNum++;
}

// 23.1 间隔定时器
void test_get_setitimer(int argc, char *argv[]) {
    struct itimerval itv = create_itimerval();
    clock_t pre_clock;
    int max_catch_sig_num = 0;             /* Number of signals to catch before exiting */
    int catch_sig_num = 0;                 /* Number of signals so far caught */

    max_catch_sig_num = (itv.it_interval.tv_sec == 0 && itv.it_interval.tv_usec == 0) ? 1 : 3;
    mysigaction(SIGALRM, signal_handler1);

    display_time("START:  ", false);
    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer");
    }

    pre_clock = clock();
    while (true) {
        /* Inner loop consumes at least 0.5 seconds CPU time */
        while (((clock() - pre_clock) * 10 / CLOCKS_PER_SEC) < 5) {
            if (s_get_alarm) {                     /* Did we get a signal? */
                s_get_alarm = 0;
                display_time("SIGALRM:", true);
                catch_sig_num++;
                if (catch_sig_num >= max_catch_sig_num) {
                    printf("finish test_get_setitimer\n");
                    return;
                }
            }
        }

        pre_clock = clock();
        display_time("While:  ", true);
    }
}


// 23.3 为阻塞操作设置超时
void test_block_timeout(bool is_restart) {
    printf("sigaction is SA_RESTART? %d\n", is_restart); // SA_RESTART, 是否自动重启由信号处理程序中断的系统调用的标志
    #define BUF_SIZE 200
    char buf[BUF_SIZE];
    ssize_t num_read;

    mysigaction(SIGALRM, signal_handler2, is_restart);

    struct itimerval itv = create_itimerval();

    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer 1");
    }

    printf("read start\n");
    num_read = read(STDIN_FILENO, buf, BUF_SIZE);
    printf("read end  \n");

    // 取消定时器
    itv = create_itimerval(0, 0, 0, 0);
    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer 2");
    }

    /* Determine result of read() */
    if (num_read == -1) {
        if (errno == EINTR) {
            printf("Read timed out\n");
        }
        else {
            exit_("read error");
        }
    } else {
        printf("Successful read (%ld bytes): %.*s", (long) num_read, (int) num_read, buf);
    }
}


// 23.4 暂停执行一段时间
void test_sleep() {
    unsigned int remain1 = 0;
    struct timespec st, remain2;
    st.tv_sec = 5;
    st.tv_nsec = 0;

    mysigaction(SIGINT, signal_handler2);

    /* sleep(int seconds)暂停进程执行seconds秒, 可能因为捕捉到信号中断休眠.
     * return: 未休眠的秒数.
     * 可能由于系统负载原因, 内核可能会在完成sleep后的一段时间后才开始重新调度.
     *
     * nanosleep(const struct timespec request, struct timespec *remain(剩余));
     * return: 0 on 成功完成休眠, -1 on 失败或中断休眠, 因信号中断时, 会将errno置为EINTR
     * request: 指定了休眠时间
     * remain: 休眠剩余时间, 可为NULL
     *
     * nanosleep()比sleep()优势:
     *  1. 未使用信号实现该函数
     *  2. 与sleep()不同, 即使nanoslee()与alarm()或setitimer()混用, 也不会危机程序的可移植性.
     *
     * */
    while (true) {
        printf("sleep start\n");
        remain1 = sleep(st.tv_sec);

        printf("nanosleep start\n");
        remain2.tv_sec = 0;
        remain2.tv_nsec = 0;
        int tmp = nanosleep(&st, &remain2);
        if (tmp == -1 && errno != EINTR) {
            exit_("nanosleep error");
        }
        printf("sleep remain %d seconds, nanosleep remain %ld seconds %ld ns \n", remain1, remain2.tv_sec, remain2.tv_nsec);

        if (0 == remain1 && 0 == tmp) {
            break;
        }
    }
}


// 23.5 POSIX时钟
void test_posix_clock() {
    /*
     * int clock_gettime (clockid_t clock_id, struct timespec *tp);  返回针对clockid所指定的时钟返回时间
     * int clock_getres (clockid_t clock_id, struct timespec *res);  返回针对clockid所指定的时钟返回时间, 返回的精度更加准确
     * both return 0 on success, -1 on error
     * clockid_t 用于表示时钟标识符, 常见为以下值:
     *      CLOCK_REALTIME            可设定的系统级实时时钟
     *      CLOCK_MONOTONIC           不可设定的恒定态时钟
     *      CLOCK_PROCESS_CPUTIME_ID  每个进程消耗的用户和CPU时间
     *      CLOCK_THREAD_CPUTIME_ID   单个线程消耗的用户和CPU时间
     * tp, res用于存放返回值
     *
     * 设置clockid指定的时钟
     * int clock_settime (clockid_t clock_id, const struct timespec *tp)
     * return 0 on success, -1 on error
     *
     * 获取特定进程的时钟ID
     * int clock_getcpuclockid (pid_t pid, clockid_t *clock_id);
     * return 0 on success, -1 on error
     * pid: 进程/线程ID, 如果pid等于0, 返回调用进程的CPU时间时钟ID
     * clock_id: 用于存放进程时钟ID
     *
     * 获取特定线程的时钟ID
     * int pthread_getcpuclockid (pthread_t thread_id, clockid_t *clock_id);
     * return 0 on success, -1 on error
     * thread_id: 线程id, cloc
     * clock_id: 用于存放线程时钟ID
     */
    clockid_t clockid;
    timespec tp;
    tp.tv_sec, tp.tv_nsec = 1, 2;

    if (-1 == clock_getcpuclockid(0, &clockid)) {
        exit_("clock_getcpuclockid error");
    }

//    if (-1 == clock_settime(clockid, &tp)) {
//        exit_("clock_settime error");
//    }
    tp.tv_sec, tp.tv_nsec = 0, 0;

    if (-1 == clock_getres(clockid, &tp)) {
        exit_("clock_gettime error");
    }
    printf("clock_id = %d s = %f, ns = %f\n", clockid, tp.tv_sec, tp.tv_nsec);

}


// 23.6 POSIX间隔式定时器
void test_posix_timer() {
    /*
     * POSIX定时器API将定时器划分为如下几个阶段(均为系统调用)
     *      timer_create()   创建定时器, 并定义到期时对进程的通知方法;
     *      timer_settimer() 启动/停止定时器
     *      timer_delete()   删除不再需要的定时器
     * 由fork()创建的子进程不会继承POSIX定时器.调用exec()期间或进程终止时将停止并删除定时器
     *
     * int timer_create (clockid_t clockid, struct sigevent *evp, timer_t* timer_id)
     *      return 0 on success, -1 on error
     *      timer_id: 放置定时器句柄, 后续指定定时器时可使用.(timer_t 用于标识定时器)
     *      evp     : 定时器到期时, 对应用程序的通知方式
     *
     *
     *
     */


}

int main(int argc, char *argv[])
{
//    test_get_setitimer(argc, argv);
//    test_block_timeout(false);
//    test_block_timeout(true);
//    test_sleep();
//    test_posix_clock();
}