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
 *     定时器是进程规划自己在未来某一时刻接获通知的一种机制
 *     休眠则能使进程(线程)暂停执行一段时间
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

void sigaction_wrapper(int sig, sighandler_t sig_handler, int sa_flags=0) {
    struct sigaction sa;

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = sa_flags;
    sa.sa_handler = sig_handler;
    if (sigaction(sig, &sa, nullptr) == -1) {
        exit_("sigaction");
    }
}

void display_time(const char *msg, bool includeTimer) {
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
    printf("%-7s %6.2f", msg, curr.tv_sec - start.tv_sec + (curr.tv_usec - start.tv_usec) / 1000000.0);  // 程序执行时间

    if (includeTimer) {
        if (getitimer(ITIMER_REAL, &itv) == -1) {
            exit_("getitimer");
        }
        printf("  %6.2f  %6.2f",
               itv.it_value.tv_sec + itv.it_value.tv_usec / 1000000.0,        // 剩余秒数
               itv.it_interval.tv_sec + itv.it_interval.tv_usec / 1000000.0); // 间隔秒数
    }

    printf("\n");
    callNum++;
}

/*
 *  struct itimerval {
 *      struct timeval it_interval;   子字段均为0: 一次性定时器; 子字段存在非0,, 周期性定时器
 *      struct timeval it_val;        距离定时器到期剩余时间
 *  };
 *
 *  struct timeval {
 *      time_t tv_sec;           // 秒
 *      suseconds_t tv_usec;     // us, 微妙
 *  }
 */
struct itimerval create_itimerval(int iv_s=5, int iv_us=0, int ii_s=5, int ii_us=0) {
    struct itimerval itv{};
    itv.it_value.tv_sec = iv_s;
    itv.it_value.tv_usec = iv_us;
    itv.it_interval.tv_sec = ii_s;
    itv.it_interval.tv_usec = ii_us;
    return itv;
}

/*
 * include <sys/time.h>
 * // itimer = interval timer
 * int setitimer(int which,
 *               const struct itimerval *new_value,  # 常量指针, 指针指向的值不可变
 *               const struct itimerval *old_value);
 *     return 0 on success, or -1 on error
 *     which: 指定定时器类型
 *          ITIMER_REAL:     创建以真实时间倒计时的定时器,                                 到期时会产生SIGALARM 信号并发送给进程
 *          ITIMER_VIRTURAL: 创建以进程虚拟时间(用户模式下的CPU时间)倒计时的定时器,            到期时会产生SIGVTALRM信号并发送给进程
 *          ITIMER_PROF:     创建一个profiling定时器, 以进程时间(用户态与内核态CPU时间的总和), 到期时会产生SIGPROF  信号并发送给进程
 *          上述信号的默认处置均会终止进程, 进程只能拥有上述定时器中的一种, 当二次调用setitimer()时, 修改已有定时器的属性要符合参数which的类型
 *     new_value:
 *          it_val：指定距离定时器到期的剩余时间, 如果调用setitimer()时, 将it_val的两个定字段均为0, 那么会屏蔽任何已有的定时器
 *          it_interval：说明该定时器是否为周期性定时器. 如果it_interval的两个字段都为0,则为一次性定时器. 只要it_interval中的任一字段非0,
 *                       那么在定时器到期后, 都会将定时器重置为在指定间隔后再次到期
 *     old_value: 若不为NULL, 则返回定时器的前一设置
 *
 *     usage: 定时器会从it_value倒计时直到0为止, 递减为0时会将相应信号发送给进程.
 *            如果it_interval非0, 那么会再次将it_value加载至定时器, 重新开始向0倒计时
 *
 * int getitimer(int which, struct itimerval *curr_val);
 *      return 0 on success, or -1 on error
 *      usage: 了解定时器的当前状态, 距离下次到期的剩余时间
 *
 * include <unistd.h>
 * unsigned int alarm(unsigned int seconds);  简化定时器的创建, alarm:警报,报警
 *      return: 返回定时器前一设置到期的剩余秒数, 如果未设置定时器则返回0
 *      seconds: 到期的秒数, 到期后会向进程发送SIGALRM信号
 *      usage: 调用alarm()会覆盖定时器的前一个设置, alarm(0)屏蔽现有定时器
 *
 * 为了保证应用程序的可移植性, 程序设置定时器时只能二选一, setitimer()/alarm()
 *
 * setitimer()和alarm()限制
 *      针对ITIMER_REAL, ITIMER_VIRTUAL和ITIMER_PROF三类定时器, 每种只能设置一个
 *      只能通过发送信号的方式来通知定时器到期, 也不能改变到期时产生的信号
 *      如果一个间隔式定时器到期多次, 且相应信号遭到阻塞, 那么只会调用一次信号处理函数
 *      定时器的分辨率只能到达微妙级, 一些系统的硬件时钟提供了更为精细的时钟分辨率
 *
 * 定时器的调度及精度
 *      取决于当前负载和对进程的调度,系统可能会在定时器到期的瞬间(通常为几分之一秒)之后才去调度其所属进程.尽管如此, 定时器到期后仍然会恪守其规律性.
 *      例如,设置一个实时定时器每两秒到期一次, 虽然上述延迟可能会影响每个定时器事件的到达, 但系统对后续定时器到期的调度依然会严格遵循两秒的时间间隔.
 *      简单来说, 间隔式定时器不受潜在错误(延迟)影响
 *
 * 23.1 创建间隔定时器, 获取定时器状态
 */
void get_setitimer() {
    struct itimerval itv = create_itimerval();
    clock_t pre_clock;
    int max_catch_signal_num;             /* Number of signals to catch before exiting */
    int catch_signal_num ;                /* Number of signals so far caught */

    catch_signal_num = 0;
    max_catch_signal_num = (itv.it_interval.tv_sec == 0 && itv.it_interval.tv_usec == 0) ? 1 : 3;
    sigaction_wrapper(SIGALRM, signal_handler1);

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
                catch_signal_num++;
                if (catch_signal_num >= max_catch_signal_num) {
                    printf("get_setitimer finish\n");
                    return;
                }
            }
        }

        pre_clock = clock();
        display_time("While:  ", true);
    }
}

/*
 * 实时定时器的用途之一是为某个阻塞系统调用设置其处于阻塞状态的时间上限
 * block_timeout()理论上存在导致竞争条件的可能性, 如果定时器到期时处于read()调用之前, 那么信号处理函数将不会中断read.
 * 所以在这种场景下设定的超时值一般相对较大.
 * 23.3 为阻塞操作设置超时
 */
void block_timeout(int sa_flags=0) {
    #define BUF_SIZE 200
    char buf[BUF_SIZE];
    ssize_t num_read;
    struct itimerval itv = create_itimerval(5, 0, sa_flags == 0 ? 0:3, 0);

    if (setitimer(ITIMER_REAL, &itv, nullptr) == -1) {
        exit_("setitimer 1");
    }
    sigaction_wrapper(SIGALRM, signal_handler2, sa_flags);
    // 定时器到期时, SIGALRM信号处理函数中断read操作
    printf("read start\n");
    num_read = read(STDIN_FILENO, buf, BUF_SIZE);
    printf("read end  \n");

    // 取消定时器
    itv = create_itimerval(0, 0, 0, 0);
    if (setitimer(ITIMER_REAL, &itv, nullptr) == -1) {
        exit_("setitimer 2");
    }

    /* result of read() */
    if (num_read == -1) {
        if (errno == EINTR) {
            printf("read timed out\n");
        }
        else {
            exit_("read error");
        }
    } else {
        printf("read success (%ld bytes): %.*s", (long) num_read, (int) num_read, buf);
    }
}

/* sleep(int seconds)暂停进程执行seconds秒, 可能因为捕捉到信号中断休眠.
 *      return: 未休眠的秒数.
 *      可能由于系统负载原因, 内核可能会在完成sleep后的一段时间后才开始重新调度.
 *
 * nanosleep(const struct timespec request, struct timespec *remain(剩余));
 *      return: 0 on 成功完成休眠, -1 on 失败或中断休眠, 因信号中断时, 会将errno置为EINTR
 *      request: 指定了休眠时间
 *      remain: 休眠剩余时间, 可为NULL
 *
 * nanosleep()比sleep()优势:
 *      1. 未使用信号实现该函数
 *      2. 与sleep()不同, 即使nanoslee()与alarm()或setitimer()混用, 也不会影响程序的可移植性.
 *
 *
 * 23.4 暂停执行一段时间
 */
void sleep_() {
    unsigned int remain1 = 0;
    struct timespec ts, remain2;
    ts.tv_sec = 5;
    ts.tv_nsec = 0;

    sigaction_wrapper(SIGINT, signal_handler2);
    while (true) {
        printf("sleep start\n");
        remain1 = sleep(ts.tv_sec);

        printf("nanosleep start\n");
        remain2.tv_sec = 0;
        remain2.tv_nsec = 0;
        int ok = nanosleep(&ts, &remain2);
        if (-1 == ok && EINTR != errno) {
            exit_("nanosleep error");
        }
        printf("sleep remain %d seconds, nanosleep remain %ld seconds\n",
                remain1, remain2.tv_sec + remain2.tv_nsec / 1000000000);

        if (0 == remain1 && 0 == ok) {
            break;
        }
    }
}

/*
 * clockid_t 用于表示时钟标识符, 常见为以下值:
 *      CLOCK_REALTIME            可设定的系统级实时时钟
 *      CLOCK_MONOTONIC           不可设定的恒定态时钟
 *      CLOCK_PROCESS_CPUTIME_ID  每个进程消耗的用户和CPU时间
 *      CLOCK_THREAD_CPUTIME_ID   单个线程消耗的用户和CPU时间
 *
 * int clock_gettime (clockid_t clock_id, struct timespec *tp);
 *      return 0 on success, -1 on error
 *      tp:    用于存放返回值
 *      usage: 返回针对clockid所指定的时钟返回时间
 *
 * int clock_getres (clockid_t clock_id, struct timespec *res);
 *      return 0 on success, -1 on error
 *      res:   用于存放返回值
 *      usage: 返回针对clockid所指定的时钟返回时间, 返回的精度更加准确
 *
 * int clock_settime (clockid_t clock_id, const struct timespec *tp)
 *      return 0 on success, -1 on error
 *      usage: 设置clockid指定的时钟
 *
 * int clock_getcpuclockid (pid_t pid, clockid_t *clock_id);
 *      return 0 on success, -1 on error
 *      pid:     进程/线程ID, 如果pid等于0, 返回调用进程的CPU时间时钟ID
 *      clock_id:用于存放进程时钟ID
 *      usage:   获取特定进程的时钟ID
 *
 * int pthread_getcpuclockid (pthread_t thread_id, clockid_t *clock_id);
 *      return 0 on success, -1 on error
 *      thread_id: 线程id
 *      clock_id:  用于存放线程时钟ID
 *      usage:     获取特定线程的时钟ID
 *
 * 23.5 POSIX时钟
 */
void posix_clock() {
    clockid_t clockid;
    timespec tp;
    tp.tv_sec, tp.tv_nsec = 1, 2;

    if (-1 == clock_getcpuclockid(0, &clockid)) {
        exit_("clock_getcpuclockid error");
    }
    tp.tv_sec, tp.tv_nsec = 0, 0;
    if (-1 == clock_getres(clockid, &tp)) {
        exit_("clock_gettime error");
    }
    printf("clock_id = %d s = %li, ns = %li\n", clockid, tp.tv_sec, tp.tv_nsec);
}


/*
 * 编译时需要链接 -lrt
 * POSIX定时器API将定时器划分为如下几个阶段(均为系统调用)
 *      timer_create()   创建定时器, 并定义到期时对进程的通知方法;
 *      timer_settimer() 启动/停止定时器
 *      timer_delete()   删除不再需要的定时器
 * 由fork()创建的子进程不会继承POSIX定时器.调用exec()期间或进程终止时将停止并删除定时器
 *
 * int timer_create (clockid_t clockid, struct sigevent *evp, timer_t* timer_id)
 *      return 0 on success, -1 on error
 *      clockid: 可使用CLOCK_MONOTONIC, CLOCK_REALTIME, CLOCK_PROCESS_CPUTIME_ID, CLOCK_THREAD_CPUTIME_ID,
 *               clock_getcpuclockid()或pthread_getcpuclockid()返回的值
 *      timer_id: 放置定时器句柄, 后续指定定时器时可使用.(timer_t 用于标识定时器)
 *      evp     : 定时器到期时, 对应用程序的通知方式
 *
 * int timer_settime(timer_t timerid, int flags, const struct itimerspec *value, struct itimerspec *old_value);
 *      retrun 0 on success, -1 on error;
 *      imerid: 定时器句柄
 *      flags：
 *          0, 会将value.it_value视为始于timer_settime()调用时间点的相对值
 *          TIMER_ABSTIME, 那么value.it_value则是一个绝对时间(从时钟值0开始), 一旦时钟过了这一时间, 定时器会立即到期
 *     value, old_value: 定时器的新设置和定时器之前的设置, old_value可以为NULL
 *     usage: 为了启动定时器, 需要调用函数timer_settimer(), 并将value.it_value的一个或全部下属字段设为非0值, 如果之前曾经配备过定时器,
 *            timer_settimer()会将之前的设置替换掉, 定时器每次到期时, 都会按照特定的方式通知进程, 这种方式由创建定时器的timer_create()定义.
 *            如果结构it_interval包含非0值，name会用这些值来重新加载it_value结构(周期性定时器)
 *            为了解除定时器, 需要调用timer_settime(), 并将value.it_value的所有字段指定为0
 *
 * int timer_gettime(timer_t timeid, struct itimerspec * curr_value);
 *      retrun 0 on success, -1 on error
 *      curr_value： 指定的itimerspec结构中返回的是时间间隔以及距离下次定时器到期的时间, 即使是以TIMER_ABSTIME标志创建的绝对时间定时器,
 *                   在curr_value字段中返回的也是距离定时器下次到期的剩余时间值
 *                   如果返回结构curr_value.it_value的两个字段都为0, 那么定时器当前处于停止状态
 *      usage: 返回由timerid指定POSIX定时器的间隔以及剩余时间
 *
 * int timer_delete(timer_t timerid);
 *      retrun 0 on success, -1 on error;
 *      usage: 删除定时器, 每个POSIX定时器都会消耗少量的系统资源, 所以使用完毕后, 应当使用timer_delete()来移除定时器并释放这些资源.
 *             对于已启动的定时器, 会在移除前自动将其停止, 如果因定时器到期而处于pending状态的信号, 信号会保持这一状态.
 *             当进程终止时, 会自动删除所有定时器.
 * 23.6 posix间隔式定时器
 */

void notify_func(sigval sig) {
    printf("timer finish, notify thread id=%lu\n",pthread_self());
}

// 定时器到期后, 新的线程调用函数
void posix_timer_thread() {
    // 查看里面结构
    struct sigevent evp{};
    timer_t timer_id;
    clockid_t clockid;
    struct itimerspec ts{};

    ts.it_value.tv_sec = 5;
    ts.it_interval.tv_nsec = 0;
    ts.it_interval.tv_sec = 5;
    ts.it_interval.tv_nsec = 0;

    // 定时器到期时, 将notify_func以线程的形式启动,
    clockid = CLOCK_REALTIME;
    evp.sigev_notify_function = notify_func;
    evp.sigev_notify = SIGEV_THREAD;
    /* sigev_notify 可选值:
     *      SIGEV_NONE:      不提供定时器到期通知, 进程可使用timer_gettime()来监控定时器的运行情况
     *      SIGEV_SIGNAL:    定时器到期后, 为进程生成sigev_signo信号, 如果为实时信号, 那么sigev_value字段指定了信号的伴随数据
     *      SIGEV_THREAD:    定时器到期时, 将sigev_notify_function作为新线程的启动函数
     *      SIGEV_THREAD_ID: 发送sigev_signo信号给sigev_notify_thread_id所标识的线程
     */

    if (-1 == timer_create(clockid, &evp, &timer_id)) {
        exit_("timer_create");
    }
    if (-1 == timer_settime(timer_id, 0, &ts, NULL)) {
        exit_("timer_settime");
    }

    printf("main   thread id=%lu\n",pthread_self());
    while (1) {
        struct itimerspec cur{};
        if (-1 == (timer_gettime(timer_id, &cur))) {
            exit_("timer_gettime");
        } else {
            printf("remain %li second\n", cur.it_value.tv_sec);
        }

        char buf[10];
        read(STDIN_FILENO, buf, 10);
        if (strcmp(buf, "exit\n") == 0) {
            break;
        }
    }
    if (-1 == timer_delete(timer_id)) {
        exit_("timer_delete");
    }
}

// 定时器到期后, 新的线程调用函数
void posix_timer_signal() {
    // 查看里面结构
    struct sigevent evp{};
    timer_t timer_id;
    clockid_t clockid;
    struct itimerspec ts{};

    ts.it_value.tv_sec = 5;
    ts.it_interval.tv_nsec = 0;
    ts.it_interval.tv_sec = 5;
    ts.it_interval.tv_nsec = 0;

    // 定时器到期时, 发送SIGINT信号
    clockid = CLOCK_REALTIME;
    evp.sigev_signo = SIGINT;
    sigaction_wrapper(SIGINT, signal_handler2);

    if (-1 == timer_create(clockid, &evp, &timer_id)) {
        exit_("timer_create");
    }
    if (-1 == timer_settime(timer_id, 0, &ts, NULL)) {
        exit_("timer_settime");
    }

    while (1) {
        struct itimerspec cur{};
        if (-1 == (timer_gettime(timer_id, &cur))) {
            exit_("timer_gettime");
        } else {
            printf("remain %li second\n", cur.it_value.tv_sec);
        }

        char buf[10];
        read(STDIN_FILENO, buf, 10);
        if (strcmp(buf, "exit\n") == 0) {
            break;
        }
    }
    if (-1 == timer_delete(timer_id)) {
        exit_("timer_delete");
    }
}

// g++ 23.cpp -lrt
int main(int argc, char *argv[])
{
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: get_setitimer\n"
               "1: block_timeout sa_flags=0\n"
               "2: block_timeout sa_flags=SA_RESTART\n"
               "3: sleep\n"
               "4: posix_clock\n"
               "5: posix_timer_thread\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            get_setitimer();
        case 1:
            block_timeout();
            break;
        case 2:
            block_timeout(SA_RESTART);
            break;
        case 3:
            sleep_();
            break;
        case 4:
            posix_clock();
            break;
        case 5:
            posix_timer_thread();
            break;
        case 6:
            posix_timer_signal();
            break;
        default:
            printf("type error, use -h, help\n")
            ;
    }
    return 0;
}