#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

/*
 * 每个进程都有一个进程号(PID=process id), 进程号是一个正数, 用以唯一标识系统中的某个进程.
 * 进程号范围: 一般情况下, 内核常量PID_MAX=0x8000, 所以进程号最大值为0x7fff = 32676
 * Linux中init进程号为1, init进程是所有进程的始祖
 * 进程号0~299的进程号为系统进程和守护进程占用.
 * 新建进程时, 内核会按顺序将下一个可用的进程号分配给其使用，每当进程号达到32676的限制时, 内核将重置进程号计数器,
 * 从300开始分配
 * 如果子进程的父进程终止, 则子进程就会变成孤儿. init进程收养该进程, 成为该进程的父进程.
 * 可通过查看由Linux特有的/proc/PID/status文件提供的PPid字段得知每个进程的父进程
 */
int pid() {
    int pid = getpid();
    printf("pid = %d\n", pid);
    scanf("input anything exist %d", &pid);
}


/*
 * 进程的内存布局:
 *      文本段:    进程运行的机器语言指令. 文本段是只读的
 *      数据段:    全局变量和静态变量, 此段常被称为BSS段
 *      栈(stack): 动态增长和手段的段. 系统会为每个当前调用的函数分配一个栈帧. 栈帧中存储了函数的局部变量, 实参《 返回值
 *      堆(heap):  运行时动态进行内存分配的一块区域
 *      栈: 地址由高 -> 低
 *      堆: 地址由低 -> 高
 * register 寄存器
 */


/*
 * 命令行参数
 * 通过Linux系统专有的/proc/PID/cmdline可以读取进程的命令行参数, 每个参数都以空字节终止
 */
void env() {
    /*
     *  char * getenv(const char *varname) 存在返回对应的值, 不存在返回NULL
     */
    char* env_name = (char *) "PATH";
    char* not_exist_env_name = (char*) "NOT_EXIST_VAR_NAME";
    printf("env var %s=%s\n", env_name, getenv(env_name)); // 获取环境变量的值
    printf("env var %s=%s\n", not_exist_env_name, getenv(not_exist_env_name)); // 获取环境变量的值
}


int main() {
//    pid();
    env();
    return 0;
}