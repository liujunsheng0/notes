// 程序的执行

#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <cerrno>
#include <sys/wait.h>

extern char **environ;

/*
 * int execve (const char *path, char *const argv[], char *const envp[]);
 *      return: 0 on success, -1 on error
 *      usage:  将新程序加载到某一进程的内存空间, 丢弃旧有程序, 进程的堆栈, 数据段会被新程序替换, 新程序从main开始执行
 *              excc**相关的函数都是构建于execve之上的
 *      path:   新程序路径名字
 *      argc:   命令参数, 以NULL结束
 *      envp:   环境列表,字符串格式为name=value
 *      notice: 由fork()生成的子进程对execve()的调用最为频繁, 因为会替换堆栈等数据.
 *              调用execve()后, 因为同一进程依然存在, 所以进程ID保持不变.
 *              调用execve后, 如果顺利的话, 老程序中execve后的代码不会执行
 *
 * ps: Linux所特有的/proc/PID/exe是一个符号链接, 对应正在执行程序的绝对路径名
 */
// 通过execve调用了execve_process()函数
void execve_(char* path) {
    char *argv[] = {path, "1", "hello world", "goodbye", NULL};  // List must be NULL-terminated
    char *envp[] = {"NAME=lilei", "AGE=15", NULL };
    /* Execute the program specified */
    execve(path, argv, envp);  // 成功执行, 不会执行后面的代码
    // If we get here, something went wrong
    printf("path=%s, execve error, msg=%s", path, strerror(errno));
}

void execve_process(int argc, char* argv[]) {
    /* Display argument list */
    for (int j = 0; j < argc; j++) {
        printf("argv[%d] = %s\n", j, argv[j]);
    }
    /* Display environment list */
    for (char **ep = environ; *ep != NULL; ep++) {
        printf("environ: %s\n", *ep);
    }
}


/*
 * 解释器: 能够读取并执行文本格式命令的程序/交互执行, 如python, awk, sed, ruby, shell
 *        内核运行解释器脚本的方式与二进制程序无异, 脚本需要满足以下条件:
 *          1. 赋予脚本可执行权限
 *          2. 文件的起始行必须制定运行脚本解释器的路径名, 格式如下: #!interpreter-path [optional-arg], 不得超过127个字符
 *          如 test.py
 *          #!/usr/bin/python
 *          import os
 *          print os.environ
 *          chmod 744 test.py, ./test.py
 * 解释器脚本的执行:
 *      如果检测到#!开始, 就会取该行剩下的部分, 按照如下参数列表来执行解释器程序:
 *      interpreter-path [optional-arg] script-path arg...
 */
/*
 * 执行shell命令 int system(const char* command);
 * 以下为system的简易实现
 */
int system_(char *command)
{
    int status;
    pid_t child_pid;

    switch (child_pid = fork()) {
        case -1: /* Error */
            return -1;

        case 0: /* Child */
            execl("/bin/sh", "sh", "-c", command, nullptr);
            _exit(EXIT_FAILURE);                     /* Failed exec */
        default: /* Parent */
            if (waitpid(child_pid, &status, 0) == -1) {
                status = -1;
            }
    }
    return status;
}

int main(int argc, char* argv[]) {
    if (argc > 1 && (!strcmp("-h", argv[1]) || !strcmp("help", argv[1]) || !strcmp("--help", argv[1]))) {
        printf("argv[1] ==\n"
               "0: execve_()\n"
               "1: execve_process()\n"
               "2: system()");
        return 0;
    }
    int type = argc > 1 ? atoi(argv[1]):0;
    switch (type) {
        case 0:
            execve_(argv[0]);
            break;
        case 1:
            execve_process(argc, argv);
            break;
        case 2:
            char* cmd = (char*)(argc < 3 ? "ls" : argv[2]);
            system_(cmd);
            break;
    }
    return 0;
}