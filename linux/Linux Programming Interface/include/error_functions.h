//
// Created by Administrator on 2019/3/1.
// 错误诊断函数
//

#ifndef LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H
#define LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H


/*
 * 这个属性告诉编译器函数不会返回，这可以用来抑制关于未达到代码路径的错误。 C库函数abort（）和exit（）都使用此属性声明：
 * extern void exit(int)   __attribute__((noreturn));
 * extern void abort(void) __attribute__((noreturn));
 */
#ifdef __GNUC__
#define NORETURN __attribute__ ((__noreturn__))
#else
#define NORETURN
#endif // __GNUC__


// 打印与当前errno对应的错误信息 + 参数列表指定的格式化输出 + 换行符
void errMsg(const char* format, ...) NORETURN;

// errMsg()  + 退出程序
void errExit(const char* format, ...) NORETURN;

// 与errExit类似, 但是使用的是给定的错误号 err_num
void errExitEn(int err_num, const char* format, ...) NORETURN;

// 只打印错误信息
void fatal(const char* format, ...) NORETURN;

// 命令行参数使用方面的错误
void usageErr(const char* format, ...) NORETURN;

#endif //LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H
