/*
 * 监控文件事件, 自内核2.6.13起, Linux开始提供inotify机制, 以允许应用程序监控文件事件
 * inotify机制可用于监控文件或目录, 当监控目录时, 与路径自身及其所含文件相关的事件都会通知给应用程序
 * inotify监控机制为非递归, 若应用程序有意控制整个目录子树内的事件, 需要对该树中的每个目录发起inotify_add_watch()调用
 * (即只监控当前目录的变化)
 * 应用程序在结束监控时会关闭inotify文件描述符, 自动清除与inotify实例相关的所有监控项
 *
 *
 * 以下均为系统调用
 * #include<sys/inotify.h>
 * int inotify_init();
 *      return descriptor on success, -1 on error
 *      创建新的inotify实例, 返回的文件描述符用于表示inotify实例
 *
 * int inotify_add_watch(int fd, const char *path, uint_32 mask);
 *      return watch descriptor on success, or -1 on error, 返回被监控文件的描述符
 *      向inotify实例中新增/修改监控项, 必须有文件的读权限, 重复添加相同路径的文件, 视为修改
 *      fd:   inotify实例
 *      path: 要用绝对路径, 欲创建或修改的监控项所对应的文件, 如果文件已添加过, 视为修改
 *      mask: 掩码, 针对path定义了意欲监控的事件
 *            IN_ACCESS         文件被访问
 *            IN_ATTRIB	        文件属性发生变化(文件元数据改变, 如权限, 链接计数, 扩展属性, 用户ID或组ID等)
 *            IN_CLOSE_WRITE	关闭以write方式打开的文件
 *            IN_CLOSE_NOWRITE	关闭以非write方式打开的文件
 *            IN_CREATE	        在受监控目录内创建了文件/目录
 *            IN_DELETE	        在受监控目录内删除了文件/目录
 *            IN_DELETE_SELF	被监测的文件/目录被删除
 *            IN_MODIFY	        文件被修改
 *            IN_MOVE_SELF	    移动受监测的文件或目录
 *            IN_MOVED_FROM	    文件移出被监测的目录
 *            IN_MOVED_TO	    文件移入被监测的目录
 *            IN_OPEN	        文件被打开
 *         上述flag的集合
 *            IN_ALL_EVENTS	    以上所有flag的集合
 *            IN_MOVE	        IN_MOVED_TO + IN_MOVED_FROM
 *            IN_CLOSE	        IN_CLOSE_WRITE + IN_CLOSE_NOWRITE
 *         不常用的flag
 *            IN_DONT_FOLLOW	不对符号链接解引用, 监控符号链接自身
 *            IN_MASK_ADD	    将事件追加到pathname的当前监控掩码
 *            IN_ONESHOT	    只监测一个事件, 事件发生后, 被监控项会从监控列表中消失
 *            IN_ONLYDIR	    只监测目录
 *            IN_IGNORED	    监控项被内核或应用程序移除
 *            IN_ISDIR	        发生事件的是一个目录
 *            IN_Q_OVERFLOW	    Event队列溢出
 *            IN_UNMOUNT	    文件系统unmount
 *
 * int inotify_rm_watch(int fd, uint32_t wd);
 *      return 0 on success, or -1 on error
 *      从fd中删除wd指定的监控项
 *      fd: inotify实例, 即inotify_init()的返回值
 *      wd: 向inotify实例中添加需要被监控的描述符, 即inotify_add_watch()的返回值
 *
 * 将监控项在监控列表中登记后, 应用程序可用read()从inotify文件描述符中读取事件, 以判定发生了哪些事件
 * 事件发生后, 每次调用read()会返回一个缓冲区, 内含一个/多个如下结构
 * read()会阻塞下去, 直至有事件发生, 除非对文件描述符设置了O_NONBLOCK状态标志
 * struct inotify_event {
 *      int      wd;       Watch descriptor, 发生事件的监控描述符
 *      uint32_t mask;     Mask of events
 *      uint32_t cookie;   Unique cookie associating related events (for rename(2))
 *                         使用该字段可将相关事件联系到一起, 目前只有对文件重命名时才会用到该字段
 *      uint32_t len;      Size of name field
 *      char     name[];   Optional null-terminated name
 *  };
 *  单个inotify事件的长度: sizeof(struct inotify_event) + len，如果传递给read()的缓冲区过小, 无法容纳一个inotify_event结
 *  构, read()调用将以失败告终. 所以传递给read()的缓存区至少为sizeof(struct inotify_event) + NAME_MAX + 1
 *      NAME_MAX: 文件名的最大长度
 *      1: 终止字符, '\0'
 *
 * 从inotify文件描述符中读取的事件根据事件发生顺序形成一个有序队列.
 * 在文件队列的末尾追加一个新事件时, 如果此事件与队列尾部事件拥有相同的wd, mask, cookie, mask值, 那么内核会将两者合并,
 * 之所以这么做, 是因为很多应用程序并不关注事件的反复出现, 丢弃多余的事件能降低内核维护事件队列所需的内存. 这也意味着
 * 使用inotify将无法可靠判定出周期性事件的发生次数或频率
 *
 *
 * 队列限制和/proc文件
 * 因为inotify事件做了排队处理, 需要消耗内核内存, 所以, 内核会对inotify机制的操作施以各种限制,
 * root用户可在/proc/sys/fs/inotify中的三个文件来调整限制
 *      max_queued_events，默认为16384
 *          调用inotify_init()时, 该值作为实例队列中事件数量上限, 超出该值, 将生成IN_Q_OVERFLOW事件, 并丢弃多余的事件.
 *          溢出事件的wd字段值为-1
 *      max_user_instances, 默认为128
 *         每个真实用户ID创建inotify实例数量的限制值
 *      max_user_watches, 默认为8192
 *         每个真实用户ID创建的监控数量的限制值
 *
 *
 */

#include <sys/inotify.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include "error_functions.h"

/* Display information from inotify_event structure */
void displayInotifyEvent(struct inotify_event *i) {
    printf("    wd =%2d; ", i->wd);
    if (i->cookie > 0)
        printf("cookie =%4d; ", i->cookie);

    printf("mask = ");
    if (i->mask & IN_ACCESS)        printf("IN_ACCESS ");
    if (i->mask & IN_ATTRIB)        printf("IN_ATTRIB ");
    if (i->mask & IN_CLOSE_NOWRITE) printf("IN_CLOSE_NOWRITE ");
    if (i->mask & IN_CLOSE_WRITE)   printf("IN_CLOSE_WRITE ");
    if (i->mask & IN_CREATE)        printf("IN_CREATE ");
    if (i->mask & IN_DELETE)        printf("IN_DELETE ");
    if (i->mask & IN_DELETE_SELF)   printf("IN_DELETE_SELF ");
    if (i->mask & IN_IGNORED)       printf("IN_IGNORED ");
    if (i->mask & IN_ISDIR)         printf("IN_ISDIR ");
    if (i->mask & IN_MODIFY)        printf("IN_MODIFY ");
    if (i->mask & IN_MOVE_SELF)     printf("IN_MOVE_SELF ");
    if (i->mask & IN_MOVED_FROM)    printf("IN_MOVED_FROM ");
    if (i->mask & IN_MOVED_TO)      printf("IN_MOVED_TO ");
    if (i->mask & IN_OPEN)          printf("IN_OPEN ");
    if (i->mask & IN_Q_OVERFLOW)    printf("IN_Q_OVERFLOW ");
    if (i->mask & IN_UNMOUNT)       printf("IN_UNMOUNT ");
    printf("\n");

    if (i->len > 0)
        printf("        name = %s\n", i->name);
}

#define NAME_MAX 128
#define BUF_LEN (10 * (sizeof(struct inotify_event) + NAME_MAX + 1))
int main(int argc, char *argv[])
{
    int inotifyFd, wd, j;
    char buf[BUF_LEN];
    ssize_t numRead;
    char *p;
    struct inotify_event *event;
    char files[][30] = {"../data/test.txt", "../data/"};
    int size = 2;

    inotifyFd = inotify_init();                 /* Create inotify instance */
    if (inotifyFd == -1)
        errExit("inotify_init");

    /* For each command-line argument, add a watch for all events */

    for (j = 1; j < size; j++) {
        wd = inotify_add_watch(inotifyFd, files[j], IN_ALL_EVENTS);
        if (wd == -1)
            errExit("inotify_add_watch");

        printf("Watching %s using wd %d\n", files[j], wd);
    }

    for (;;) {                                  /* Read events forever */
        numRead = read(inotifyFd, buf, BUF_LEN);
        if (numRead == 0)
            fatal("read() from inotify fd returned 0!");

        if (numRead == -1)
            errExit("read");

        printf("Read %ld bytes from inotify fd\n", (long) numRead);

        /* Process all of the events in buffer returned by read() */

        for (p = buf; p < buf + numRead; ) {
            event = (struct inotify_event *) p;
            displayInotifyEvent(event);

            p += sizeof(struct inotify_event) + event->len;
        }
    }
    return 0;
}