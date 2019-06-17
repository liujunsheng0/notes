// 线程安全和线程存储

#include <cstdio>
#include <pthread.h>
#include <cstring>
#include <string>
#include <zconf.h>
#include <ctime>
#include <error_functions.h>

#define SIZE 3
#define MAX_ERROR_LEN 2560           /* Maximum length of string in per-thread buffer returned by strerror() */

void exit_(const std::string &msg) {
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(errno));
    _exit(EXIT_FAILURE);
}

/*
 * 一次性初始化: 不管创建了多少线程, 初始化动作只能发生一次(场景:使用了全局变量的库函数)
 * int pthread_once (pthread_once_t *once_control, void (*init) (void))
 *      return: 0 on success, errno on error
 *      usage: 利用once_control的状态, 函数pthread_once()可以确保只会执行一次init指向的函数
 *      once_control: 可用PTHREAD_ONCE_INIT初始化, 该函数的首次调用将修改one_control指向的内容,以便后续不会再次执行init
 */
void init() {
    printf("init\n");
}
void* func(void*) {
    static pthread_once_t ponce = PTHREAD_ONCE_INIT;
    if (0 != pthread_once(&ponce, init)) {
        exit_("once_");
    }
    return nullptr;
}
void once_() {
    pthread_t tds[SIZE];

    for (pthread_t &td : tds) {
        if (0 != pthread_create(&td, nullptr, func, nullptr)) {
            exit_("create error");
        }
    }
    for (pthread_t &td : tds) {
        if (0 != pthread_join(td, nullptr)) {
            exit_("join");
        }
    }
}

/*
 * 使用线程特有数据步骤如下:
 *  1. 函数创建一个key, 用以将不同函数使用的线程特有数据区分开来.
 *     pthread_key_create()创建此键, 且只需要在首个调用该函数的线程中创建一次, 可配合 pthread_once
 *     键在创建时并未分配任何线程特有的数据块
 *  2. 调用pthread_key_create的另一个目的是允许调用者指定析构函数,用于释放资源,当使用线程特有数据的线程终止时,
 *     Pthreads API会自动调用此函数, 同时将该数据块指针作为参数传入
 *  3. 函数会为每个线程创建线程特有的数据块, 通过malloc完成, 每个线程只分配一次, 且只会在线程初次调用此函数时分配.
 *
 * 为线程特有数据创建一个新键, 通过key所指向的缓冲区返回给调用者
 * int pthread_key_create (pthread_key_t *key, void (*destr_function) (void *))
 *      return 0 on success, errno on error
 *      destr_function: 线程终止时与key的关联值不为NULL, API会自动执行析构函数, 并将与key的关联值作为参数传入析构函数.
 *                      如果无需调用析构函数, 可将参数置为NULL
 * destroy KEY
 * int pthread_key_delete (pthread_key_t key);
 *      return 0 on success, errno on error
 *
 * return current value of the thread-specific data slot identified by KEY.
 * void *pthread_getspecific (pthread_key_t key);
 *
 * store POINTER in the thread-specific data slot identified by KEY
 * int pthread_setspecific (pthread_key_t key, const void *pointer)
 *      return 0 on success, errno on error
 *
 * 总结: 1. 首先为每个函数分配地址, key就固定了
 *      2. 当不同的线程调用使用了线程特有数据的函数时, 类似于 dict: key = thread id, value = address
 *         so: 每次取数据时等于: global[key][thread id], 如果为NULL, 申请内存....
 *      3. 线程结束后, 如果需要, 释放global[key][thread id]所指向的内存
 */

static pthread_once_t once = PTHREAD_ONCE_INIT;
static pthread_key_t strerror_key;
static __thread char BUF[MAX_ERROR_LEN] = "12345";

/* free thread-specific data buffer */
static void destructor(void *buf) {
    printf("free buf\n");
    free(buf);
}
/* one-time key creation function */
static void create_key(void) {
    printf("create key\n");
    // allocate a unique thread-specific data key and save the address of the destructor for thread-specific data buffers
    // 线程结束后, 会自动调用destructor函数
    if (0 != pthread_key_create(&strerror_key, destructor))
        exit_("pthread_key_create");
}
// 使用线程特有数据, 使得strerror为线程安全函数
char *pthread_strerror(int err) {
    int s;
    char *buf;
    /* make first caller allocate key for thread-specific data */
    s = pthread_once(&once, create_key);
    if (s != 0)
        exit_("pthread_once");
    buf = (char *)pthread_getspecific(strerror_key);
    /* if first call from this thread, allocate buffer for thread, and save its location */
    if (buf == nullptr) {
        printf("malloc memory\n");
        buf = (char*)malloc(MAX_ERROR_LEN);
        if (buf == nullptr) {
            exit_("malloc");
        }
        s = pthread_setspecific(strerror_key, buf);
        if (s != 0) {
            exit_("pthread_setspecific");
        }
    }

    if (err < 0 || err >= _sys_nerr || _sys_errlist[err] == nullptr) {
        snprintf(buf, MAX_ERROR_LEN, "Unknown error %d", err);
    } else {
        strncpy(buf, _sys_errlist[err], MAX_ERROR_LEN - 1);
        buf[MAX_ERROR_LEN - 1] = '\0';          /* ensure null termination */
    }
    return buf;
}

/*
 * 线程局部存储, 类似于线程特有数据, 线程局部存储提供了持久的每线程存储
 * 声明如下:
 *      static __thread char buf[size];
 * 但凡有这种声明的变量, 每个线程都会拥有一份对变量的拷贝. 线程局部存储中的变量将一直存在, 直至线程终止, 届时将自动释放
 */
char *pthread_strerror2(int err) {
    // 每个线程会拥有BUF的拷贝, 并不会影响原有数据
    if (err < 0 || err >= _sys_nerr || _sys_errlist[err] == nullptr) {
        snprintf(BUF, MAX_ERROR_LEN, "Unknown error %d", err);
    } else {
        strncpy(BUF, _sys_errlist[err], MAX_ERROR_LEN - 1);
        BUF[MAX_ERROR_LEN - 1] = '\0';          /* ensure null termination */
    }
    return BUF;
}

void* thread_func(void *n) {
    int err = *((int*)n);
    printf("pthread_strerror  error = %d, description = %s\n", err, pthread_strerror(err));
    printf("pthread_strerror2 error = %d, description = %s\n", err, pthread_strerror2(err));
    return nullptr;
}
void pthread_strerror_test() {
    setbuf(stdout, nullptr);
    pthread_t tds[SIZE];
    int args[] = {1, 12, 13};

    for(int i = 0; i < SIZE; i++) {
        if (0 != pthread_create(&tds[i], nullptr, thread_func, (void*)(args + i))) {
            exit_("create");
        }
    }
    for (pthread_t t : tds) {
        if (0 != pthread_join(t, nullptr)) {
            exit_("join");
        }
    }
    printf("BUF = %s", BUF);
}

int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: once_\n"
               "1: pthread_strerror_test\n");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            once_();
            break;
        case 1:
            pthread_strerror_test();
            break;
        default:
            ;
    }
    return 0;
}
