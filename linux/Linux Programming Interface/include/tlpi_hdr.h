//
// Created by Administrator on 2019/3/1.
// 学习过程中用到的头文件
//

#ifndef TLPI_HDR_H
#define TLPI_HDR_H

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  // 系统调用原型方法
#include <errno.h>   // 包含了全局变量errno, 值为错误的具体类型
                     // 使用errno原因, C函数返回值只有一个, 如果返回类型为void*, 只知道发生了错误, 但是并不知道错误的具体原因
#include <string.h>

typedef enum {FALSE, TRUE} Boolean;
#define min(x, y) ((m) < (n) ? (m): (n))
#define min(x, y) ((m) < (n) ? (n): (m))

#endif  // ifndef TLPI_HDR_H
