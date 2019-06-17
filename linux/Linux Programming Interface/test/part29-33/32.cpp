// 线程取消

#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <pthread.h>
#include <cerrno>
#include <zconf.h>
#include <string>

void exit_(const std::string &msg, int err=-1) {
    if (err == -1) {
        err = errno;
    }
    printf("error %s, errno=%d, %s\n", msg.c_str(), errno, strerror(err));
    _exit(EXIT_FAILURE);
}

/*
 * ps: 无特殊声明, 线程相关的函数一般都是: return 0 on success, errno on error
 * int pthread_cancel (pthread_t __th);
 *      notice: 发出请求后, 函数立即返回, 不会等待目标线程的退出
 *
 * 会将调用线程的取消状态置为state的值(取消状态)
 * int pthread_setcancelstate (int state, int *oldstate);
 *      state: PTHREAD_CANCEL_ENABLE
 *                  线程可以取消
 *             PTHREAD_CANCEL_DISABLE
 *                  线程不可取消, 如果收到取消请求, 将取消请求挂起, 直至将线程的取消状态置为启用
 *      oldstate: 原来的state, 如不需要可为NULL
 *
 * 设置对线程取消请求的处理类型(取消类型)
 * int pthread_setcanceltype (int type, int *oldtype);
 *      type: PTHREAD_CANCEL_ASYNCHRONOUS     可能会在任何时间点取消线程
 *            PTHREAD_CANCEL_DEFERRED(默认值)  取消请求保持至挂起状态, 直至到达取消点.
 *      oldtype: 原来的type, 如不需要可为NULL
 *
 * 取消点:若线程取消状态=PTHREAD_CANCEL_ENABLE&类型=PTHREAD_CANCEL_DEFERRED, 仅当线程抵达某个取消点时, 取消请求才会起作用.
 * 以下函数必为取消点:
 *      accept(), sleep(), open(), close(), send(), read(), wait(), ......
 *
 * 如果函数中不包含取消点, 此时线程可能永远不会响应取消请求. pthread_testcancel会产生取消点
 * void pthread_testcancel (void);
 *
 * 线程在执行到取消点取消, 如果只是草草收场, 可能导致可怕的后果(如死锁). 为了避免问题, 线程可以设置一个/多个线程清理函数. 当线程取消时自动执行
 * 每个线程都可以拥有清理函数栈, 当线程遭取消时, 会沿栈自顶向下执行清理函数.
 * void pthread_cleanup_push(void (*routine)(void*), void *arg);
 *      usage: 向清理栈中添加函数
 * void pthread_cleanup_pop(int execute);
 *      usage: 清理栈顶函数
 *      execute: 非0, 清理后, 立即执行
 *      notice: pthread_cleanup_push与pthread_cleanup_pop一一对应, 配对的宏, 内嵌了函数
 */


void *thread_func(void* arg){
    int state = *((int*)arg);
    pthread_setcancelstate(state, nullptr);
    printf("state = %d, New thread started\n", state);     /* May be a cancellation point */
    for (int j = 1; j < 6; j++) {
        printf("loop %d\n", j);         /* May be a cancellation point */
        sleep(1);                       /* A cancellation point */
    }
    return nullptr;
}

void cancel(int state) {
    pthread_t thr;
    int s;
    void *res;

    s = pthread_create(&thr, nullptr, thread_func, &state);
    if (s != 0) {
        exit_("pthread_create", s);
    }

    sleep(2);

    printf("pthread_cancel\n");
    s = pthread_cancel(thr);
    if (s != 0) {
        exit_("pthread_cancel", s);
    }


    s = pthread_join(thr, &res);
    if (s != 0) {
        exit_("pthread_join", s);
    }

    if (res == PTHREAD_CANCELED) {
        printf("thread was canceled\n");
    }
    else {
        printf("thread was not canceled\n");
    }
}


pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
int glob = 0;                    /* Predicate variable */
void cleanup_handler(void *arg) {
    int s;
    printf("cleanup: freeing block at %p\n", arg);
    if (arg != nullptr) {
        free(arg);
    }
    printf("cleanup: unlocking mutex\n");
    s = pthread_mutex_unlock(&mtx);
    if (s != 0) {
        exit_("pthread_mutex_unlock", s);
    }
}

void cleanup_printf(void*) {
    printf("cleanup: cleanup_printf\n");
}

void *thread_func_clean(void *arg) {
    int s;
    void *buf = nullptr;                   /* Buffer allocated by thread */

    buf = malloc(0x10000);              /* Not a cancellation point */
    printf("thread:  allocated memory at %p\n", buf);

    s = pthread_mutex_lock(&mtx);       /* Not a cancellation point */
    if (s != 0) {
        exit_("pthread_mutex_lock", s);
    }

    pthread_cleanup_push(cleanup_handler, buf);
    pthread_cleanup_push(cleanup_printf, nullptr);

    while (glob == 0) {
        s = pthread_cond_wait(&cond, &mtx);     /* A cancellation point */
        if (s != 0) {
            exit_("pthread_cond_wait", s);
        }
    }

    pthread_cleanup_pop(1);             /* pop后, 立即执行清理函数 */
    printf("thread:  condition wait loop completed\n");
    pthread_cleanup_pop(1);             /* Executes cleanup handler */
    return nullptr;
}

void clean() {
    pthread_t thr;
    void *res;
    int s;

    setbuf(stdout, NULL);
    s = pthread_create(&thr, nullptr, thread_func_clean, nullptr);
    if (s != 0)
        exit_("pthread_create", s);

    sleep(2);                   /* Give thread a chance to get started */

    s = pthread_mutex_lock(&mtx);   /* See the TLPI page 679 erratum */
    if (s != 0) {
        exit_("pthread_mutex_lock", s);
    }
    glob = 1;
    s = pthread_mutex_unlock(&mtx); /* See the TLPI page 679 erratum */
    if (s != 0) {
        exit_("pthread_mutex_unlock", s);
    }

    s = pthread_cond_signal(&cond);
    if (s != 0) {
        exit_("pthread_cond_signal", s);
    }

    s = pthread_join(thr, &res);
    if (s != 0) {
        exit_("pthread_join", s);
    }
    if (res == PTHREAD_CANCELED) {
        printf("main:    thread was canceled\n");
    } else {
        printf("main:    thread terminated normally\n");
    }
}


int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: cancel(PTHREAD_CANCEL_ENABLE) \n"
               "1: cancel(PTHREAD_CANCEL_DISABLE)\n"
               "2: ");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            cancel(PTHREAD_CANCEL_ENABLE);
            break;
        case 1:
            cancel(PTHREAD_CANCEL_DISABLE);
            break;
        case 2:
            clean();
            break;
        default:
            ;
    }
    return 0;
}