#include <stdio.h>
#include <sys/time.h>

/*
 * struct timeval {
 *      time_t tv_sec;      从UTC 1970-1-1 0:0:0经过的秒数, 时间戳
 *      suseconds tv_usec;  微秒
 *  };
 *
 * gettimeofday(timeval *tv, timezone *tz);
 *      返回日历时间
 *      tz是历史产物, 目前已经弃用, 始终将其至为NULL
 *
 * time(time_t)
 *      返回时间戳, 与gettimeofday()所返回的tv参数中tv_sec字段的数值相同, 失败返回-1
 *
 */
void time_test() {
    timeval tv;
    gettimeofday(&tv, NULL);
    time_t tt = time(NULL);

    printf("second = %ld, us = %ld\n", tv.tv_sec, tv.tv_usec);
    printf("second = %ld\n", tt);
}

int main() {
    time_test();
    return 0;
}