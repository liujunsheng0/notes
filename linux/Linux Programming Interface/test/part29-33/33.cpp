// 线程更多细节

#include <pthread.h>
#include <bits/sigthread.h>

/*
 * 线程栈: 每个线程都有属于自己的线程栈, x32一般为2MB, x64下要大一些. 主线程的栈的空间要大很多.
 * 设置栈的属性, 但是设置后会降低程序的可移植性
 * pthread_attr_setstacksize (pthread_attr_t *attr, size_t stacksize)
 *
 *
 * 不要将线程与信号混合使用, 多线程的程序设计应该避免使用信号, 如果多线程应用必须处理信号的话, 最简洁的方法是所有的线程都阻塞信号.
 * 创建一个专门的线程来接收信号.
 *
 * 信号模型: 进程层面/线程层面
 *  1. 信号动作属于进程层面, 如果进程中的任一线程收到了默认动作为stop/terminate, 那么将停止/终止该进程的所有线程
 *  2. 对信号的处理属于进程层面, 进程中的所有线程共享对每个信号的处置设置, 如果某一线程指定了线程处理函数, 那么任何线程都会使用该信号处理函数,
 *     与之类似, 如果队形的处置设置为忽略, 那么所有线程都会忽略该信号
 *  3. 信号的发送可针对进程, 也可针对特定线程, 当满足以下三者情况之一是属于面向线程的
 *      1) 信号的产生源于线程上下文中对特定硬件执行的执行(即硬件异常, 如SIGBUS, SIGFPE, SIGSEGV)
 *      2) 当线程试图对已经断开的管道进行写操作时所产生的SIGPIPE信号
 *      3) pthread_kill(), pthread_sigqueue()发出的信号
 *     由其他机制产生的信号都是面向进程的, 如其他进程调用kill(), sigqueue(), 用户输入特殊终端字符产生的信号(如SIGINT),
 *     定时器到期等.
 *  4. 当多线程程序收到一个信号后, 内核会任选一线程来接收信号, 并在该线程中调用信号处理函数.
 *  5. 信号掩码是针对每个线程而言的. 各个线程可独立阻止/放行信号.
 *  6. 针对整个进程/每条线程所挂起的信号, 内核都分别维护有记录. 调用函数sigpending()会返回进程和当前线程所挂起信号的并集.
 *  7. 如果信号处理程序中断了pthread_mutex_lock()的调用, 那么该调用总是会自动重新开始.
 *  8. 备选信号栈是每个线程特有的, 新创建的线程并不从创建者处继承备选信号栈.
 *
 *  pthread_kill();    向线程发送信号
 *  pthread_sigmask(); 操作线程的信号掩码
 */