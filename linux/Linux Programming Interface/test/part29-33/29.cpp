// 线程
#include <cerrno>
#include <pthread.h>
#include <stdio.h>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <zconf.h>
#include <string>

void exit_(const std::string &msg) {
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(errno));
    _exit(EXIT_FAILURE);
}

/* 线程是允许应用程序并发执行多个任务的一种机制, 一个进程可以包含多个线程, 同一进程里的所有线程都会独立执行, 且共享同一份全局内存区域
 * 其中包括初始化数据段,未出赎回数据段,堆内存段.
 * 同一进程的多个线程可以并发执行, 在多处理器环境下,多个线程可以同时并行, 如果一个线程因等待IO而糟阻塞, 其他线程依然可以执行
 * 线程共享的属性:
 *      全局内存
 *      进程ID和父进程ID
 *      进程组ID, 会话ID
 *      控制终端
 *      打开的文件描述符
 *      由fcntl()创建的记录锁
 *      信号处置
 *      资源消耗
 * 各个线程所独有的属性<
 *      线程ID

 *      errno变量, errorno是一个函数, 返回可修改的左值, 获取时都会带来一个额外的开销
 *      栈, 本地变量和函数的调用链接信息
 *      信号掩码
 *      线程特有数据
 *      备选信号栈
 *      实时调度测量和优先级
 *      CPU亲和力
 *      浮点型环境
 *      能力
 * 线程数据类型
 *      pthread_t              线程ID
 *      pthread_mutex_t        互斥对象
 *      pthread_mutexattr_t    互斥属性对象
 *      pthread_cond_t         条件变量
 *      pthread_condattr_t     条件变量的属性对象
 *      pthread_key_t          线程特有的数据键
 *      pthread_once_t         一次性初始化控制上下文
 *      pthread_attr_t         线程的属性对象
 * Pthreads函数返回值: 成功返回0, 失败返回正整数, 失败时返回值等于errno的值(使用errno会有额外开销,需要errno时,使用该返回值)
 * 启动程序时, 产生的进程只有单条线程, 为初试线程或主线程
 *
 * 创建线程
 * int pthread_create (pthread_t *thread,      const pthread_attr_t *attr,
 *                     void *(*start_func) (void*), void *arg);
 *      return: 0 on success, 正整数 on error(等于errorno)
 *      usage: 新线程通过调用带有参数arg的函数start而开始执行
 *      thread: 线程id
 *      attr:   指定了新线程的各种属性, 如果为NULL, 则新线程使用默认属性
 *      start:  线程执行函数, 参数为void*, 返回值为void*, 返回值不应分配在线程栈中, 线程退出后, 线程栈的内容可能无效
 *      arg:   一般情况下, arg指向一个全局变量或堆变量, 也可以置为NULL, 如果传递多个参数, 可以指向结构体
 *      notice: 线程取消时, 返回 PTHREAD_CANCELED(一般为-1)
 * 终止线程
 *      1. 线程start函数执行return语句, 并返回值
 *      2. 调用pthread_exit()
 *      3. pthread_cancel()取消线程
 *      4. 任意线程调用exit()或者主线程执行了return语句,都会导致进程的所有线程终止
 *
 * 终止调用线程, 其返回值可由另一个线程调用pthread_join()来获取
 * void pthread_exit(void* retval);
 *      usage: 相当于在start函数中执行了return, 可在线程start函数任意处调用pthread_exit()
 *      retval: 指定了线程的返回值, retval所指向的内容不应分配在线程栈中, 因为线程终止后, 无法确定线程栈的内容是否有效
 *      notice: 如果主线程调用了pthread_exit, 而非return/exit, 那么其他线程将继续运行.
 *
 * 获取自己的线程ID
 * pthread_t pthread_self();
 *
 * 检查两个线程的ID是否相同
 * int pthread_equal(pthread_t t1, pthread_t t2);
 *      return: 相等->非0值, 不相等->0
 *      notice: 必须将pthread_t作为一种不透明的数据类型加以对待, 所以使用pthread_equal()判断线程线程id是否相同
 *              linux将pthread_t定义为无符号长整型, 在其他实现中有可能是指针或结构
 *
 * 等待指定线程终止, 如果线程已经返回, 立即返回
 * int pthread_join(pthread_t thread, void **retval);
 *      return: 0 on success, 正整数 on error
 *      retval: 返回线程返回值的拷贝, 即return或pthread_exit()所指定的值, 如果线程取消返回PTHREAD_CANCELED
 *      notice: 如果创建了线程后, 未使用pthread_join, 线程终止时会产生僵尸线程, 若僵尸线程积累数过多, 进程将无法创建新的线程
 *
 * 线程的分离, 默认情况下, 线程是可连接的(joinable), 即当线程退出时, 其他线程可以通过调用pthread_join()来获取其返回值.
 * 有时, 程序员并不关心线程的返回状态, 只是希望系统在线程终止时能够自动清理并移除. 这种情况下, 可以调用pthread_detach(), 将该线程标记为处于
 * detached(分离)状态.
 * int pthread_detach(pthread_t thread);
 *      return: 0 on success, 正整数 on error
 *      usage: 线程终止时, 系统自动回收, 无需调用pthread_join
 *      notice: 一旦线程处于分离状态, 就不能使用pthread_join()来获取其状态, 也无法使其返回可连接状态
 *              其他线程调用exit()或主线程执行return时, 分离的线程也会立即终止,
 */

void* start(void*) {
    return nullptr;
}

// 测试僵尸线程
void zombie_thread() {
    std::vector<pthread_t> threads;
    while (true) {
        pthread_t thread;
        if (0 != pthread_create(&thread, nullptr, start, nullptr)) {
            break;
        }
        threads.push_back(thread);
    }
    for(auto t: threads) {
        if (0 != pthread_join(t, nullptr)) {
            printf("join error %s\n", strerror(errno));
            break;
        }
    }
    printf("after create %lu thread, can not crate thread\n", threads.size());
}


void detach() {
    pthread_t thread;
    if (0 != pthread_create(&thread, nullptr, start, nullptr)) {
        exit_("pthread create error");
    }
    if (0 != pthread_detach(thread)) {
        exit_("pthread detach error");
    }

    if (0 == pthread_join(thread, nullptr)) {
        printf("joinable thread\n");
    } else {
        printf("detach thread\n");
    }
}


void join_self() {
    int ans = pthread_join(pthread_self(), nullptr);
    if (0 != ans) {
        // join self error Resource deadlock avoided
        printf("join self error %s\n", strerror(ans));
    }
}

// ./g++ -pthread 29.cpp
int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: zombie_thread()\n"
               "1: detach()\n"
               "2: join self()");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            zombie_thread();
            break;
        case 1:
            detach();
            break;
        case 2:
            join_self();
            break;
    }
    return 0;
}