//
// Created by Administrator on 2019/3/1.
// 学习过程中用到的头文件
//

#ifndef HEADER_H
#define HEADER_H

#include <sys/stat.h>    // unix/linux系统定义文件状态的文件, 里面的函数可以返回一个结构，里面包括文件的全部属性
                         // stat = display file or file system status
#include <sys/types.h>   // 基本系统数据类型
#include <fcntl.h>       // 包含了读,写,关闭文件等操作的文件
                         // fcntl = file control
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>      // 系统调用原型方法, 定义了POSIX标准名称
                         // unistd = Unix Standard
                         // 所有遵循POSIX标准的操作系统和编译器均应提供该头文件
#include <errno.h>       // 包含了全局变量errno, 值为错误的具体类型
                         // 使用errno原因, C函数返回值只有一个, 如果返回类型为void*, 只知道发生了错误, 但是并不知道错误的具体原因
#include <string.h>
#include <string>
typedef enum {FALSE, TRUE} Boolean;

typedef unsigned int uint;

#endif  // ifndef HEADER_H
