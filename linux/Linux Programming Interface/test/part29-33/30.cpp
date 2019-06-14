// 线程同步

#include <cstdio>
#include <pthread.h>
#include <cstring>
#include <string>
#include <zconf.h>
#include <ctime>

void exit_(const std::string &msg) {
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(errno));
    _exit(EXIT_FAILURE);
}

/*
 * 互斥量(mutex): 帮助线程同步对共享资源的使用, mutex=mutual exclusion(相互排斥)
 * 条件变量(condition): 允许线程相互通知共享变量的状态发生了变化
 *
 * 互斥量: 已锁定(locked)和未锁定(unlocked), 任何时候, 至多只有一个线程可以锁定该互斥量, 试图对已经锁定的互斥量加锁, 可能阻塞线程/报错失败
 *        一旦某个线程锁定了互斥量, 该线程随即成为该互斥量的所有者, 只有所有者才能给互斥量解锁.
 * 访问共享资源时:
 *      1. 针对共享资源锁定互斥量
 *      2. 访问共享资源
 *      3. 对互斥量解锁
 * int pthread_mutex_lock(pthread_mutex_t *mutex);
 * int pthread_mutex_unlock(pthread_mutex_t *mutex);
 *      return 0 on success, 正整数的errno on error
 *      notice: mutex已加锁, pthread_mutex_lock将会一直阻塞, 直到mutex解锁
 *              不要解锁处于未锁定的mutex
 *              不要解锁由其他线程锁定的mutex
 *
 * 动态初始化互斥量
 * int pthread_mutex_init (pthread_mutex_t *mutex, const pthread_mutexattr_t *mutexattr);
 *      return 0 on success, 正整数的errno on error
 *      attr: 互斥量的属性, 如果为NULL, 则互斥量的各种属性为默认值
 *      notice: 必须使用该方法初始化互斥量, 不然将导致未定义的行为
 *
 * 销毁互斥量
 * int pthread_mutex_destroy(pthread_mutex_t *mutex);
 *      return 0 on success, 正整数的errno on error
 *      notice: 只有当互斥量处于未锁定状态, 且后续无任何线程企图锁定时, 将其销毁才是安全的
 *              若互斥量处于动态分配的内存区域中, 应在free此内存区域前将其销毁
 *              经过销毁的互斥量, 可调用init重新对其初始化
 *
 * 互斥量的属性:
 *  互斥量类型:
 *      PTHREAD_MUTEX_NORMAL(PTHREAD_MUTEX_DEFAULT)
 *          不具有死锁检测(自检)功能
 *      PTHREAD_MUTEX_ERRORCHECK
 *          对此类互斥量的所有操作都会执行错误检查, 运行较慢, 可以将其作为调试工具
 *      PTHREAD_MUTEX_RECURSIVE
 *          递归互斥量维护一个锁计数器, 当线程取得互斥量时, 会将锁计数器+1, 解锁-1, 只有当锁计数器为0时, 才会释放该互斥量
 */
int glob = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;  // 默认初始化
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;     // 默认初始化

void *thread_add(void *arg) {
    bool lock = *((bool *) arg);
    for (int i = 0; i < 10000; i++) {
        if (lock && pthread_mutex_lock(&mutex) != 0) {
            exit_("lock error");
        }
        int loc = glob;
        loc++;
        glob = loc;
        if (lock && pthread_mutex_unlock(&mutex) != 0) {
            exit_("unlock error");
        }
    }
    return nullptr;
}
/*
 * 不加锁的时候, 结果比预期要小, 原因如下
 *  1. 线程1将glob赋值给loc, 假设glob的当前值为2000
 *  2. 线程1的时间片期满, 线程2执行
 *  3. 线程2多次循环, 假设线程2时间片到期后, glob的值为3000
 *  4. 线程1恢复执行, glob=2001, 覆盖了线程2的结果
 *  所以结果会比预期小很多
 */
void add(bool lock=false) {
    pthread_t t1, t2;
    if (pthread_create(&t1, nullptr, thread_add, &lock) != 0 ||
            pthread_create(&t2, nullptr, thread_add, &lock) != 0) {
        exit_("pthread_create");
    }
    if (pthread_join(t1, nullptr) != 0 || pthread_join(t2, nullptr) != 0) {
        exit_("join");
    }
    printf("lock = %d, glob = %d\n", lock, glob);  // should 20000
}

/*
 * 条件变量(condition, pthread_cond_t): 允许线程相互通知共享变量的状态发生了变化
 * 主要作用: 发送信号和等待
 *      发送信号: 通知一个/多个处于等待状态的线程, 某个共享变量的状态已经改变
 *      等待操作: 收到一个通知前处于阻塞状态
 * 条件变量并不保存状态信息, 只是传递程序状态信息的一种机制, 发送信号时, 若无线程等待该条件变量, 这个信号也会不了了之
 *
 * 发送信号, 只保证至少唤醒一条遭到阻塞的线程
 * int pthread_cond_signal (pthread_cond_t *cond)
 * 发送信号, 唤醒所有遭到阻塞的线程, 调用前线程持有需持有该锁, 挂起前释放锁, 满足条件后, 获取锁
 * int pthread_cond_broadcast (pthread_cond_t *cond)
 *
 * 阻塞线程, 直至收到条件变量cond通知, 调用前线程持有需持有该锁, 挂起前释放锁, 满足条件后, 获取锁
 * int pthread_cond_wait (pthread_cond_t *cond, pthread_mutex_t *mutex)
 * 如果abs制定的绝对时间间隔到期, 且无相关条件变量的通知, 返回ETIMEOUT错误
 * int pthread_cond_timedwait (pthread_cond_t *cond, pthread_mutex_t *mutex, const struct timespec *abstime);
 *      return 0 on success, 正整数的errno on error
 *
 * notice:
 *      线程在调用pthread_cond_wait()或pthread_cond_timedwait()前必须获取该锁, 并在线程挂起进入等待前解锁, 在条件满足离开
 *      pthread_cond_wait()或pthread_cond_timedwait()之前, mutex将被重新加锁, 与进入wait前的加锁动作对应. 
 */

void* produce(void*) {
    int count = 10;
    while (count-- > 0) {
        if (0 != pthread_mutex_lock(&mutex)) {
            exit_("lock error");
        }
        int num = (int)(random() % 5 + 1);
        glob += num;
        int tmp = glob;
        printf("produce  %d, size=%d\n", num, glob);
        if (0 != pthread_mutex_unlock(&mutex)) {
            exit_("unlock error");
        }
        if (0 != pthread_cond_signal(&cond)) {
            exit_("cond_broadcast error");
        }
        if (tmp > 5) {
            sleep(1);
        }
    }
    printf("*** produce finish ***\n");
    return nullptr;
}
void* customer(void*) {
    struct timespec ts;
    ts.tv_nsec = 0;
    while (true) {
        if (0 != pthread_mutex_lock(&mutex)) {
            exit_("lock error");
        }
        ts.tv_sec = time(nullptr) + 3;
        int num = (int)(random() % 3 + 1);
        if (glob - num > 0) {
            glob -= num;
            printf("customer %d, size=%d\n", num, glob);
        // 线程在调用pthread_cond_wait()或pthread_cond_timedwait()前必须获取该锁
        } else if(ETIMEDOUT == pthread_cond_timedwait(&cond, &mutex, &ts)) {
            break;
        }
        if (0 != pthread_mutex_unlock(&mutex)) {
            exit_("unlock error");
        }
    }
    printf("*** customer finish ***\n");
    return nullptr;
}
// 条件变量模拟生产者-消费者
void produce_customer() {
    pthread_t p, c;
    if (0 != pthread_create(&p, nullptr, produce, nullptr) ||
        0 != pthread_create(&c, nullptr, customer, nullptr)) {
        exit_("create error");
    }
    if (0 != pthread_join(p, nullptr) ||
        0 != pthread_join(c, nullptr)) {
        exit_("join error");
    }
}

/*
 * 动态初始化条件变量
 * int pthread_cond_init (pthread_cond_t *cond, const pthread_condattr_t *cond_attr)
 * int pthread_cond_destroy (pthread_cond_t *cond);
 *      return 0 on success, errno(正整数) on error
 *      cond_attr: 条件变量属性, 若为NULL, 则使用默认属性
 *      notice: 对已经初始化的条件变量再次初始化, 将导致未定义行为, 应避免这一做法
 *              当不在需要经由自动/动态分配的条件变量时, 应调用pthread_cond_destroy予以销毁
 *              对使用PTHREAD_COND_INITIALIZER进行静态初始化的条件变量, 无需调用pthread_cond_destroy
 *              经销毁的条件变量, 可以使用init对其进行重新初始化
 *              当没有任何线程在等待条件变量时, 将其销毁才是安全的
 */

// g++ -pthread 30.cpp
int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: thread_add\n"
               "1: \n"
               "2: ");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            add();
            glob = 0;
            add(true);
            break;
        case 1:
            produce_customer();
            break;
        default:
            break;
    }
    return 0;
}