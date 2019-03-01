//
// Created by Administrator on 2019/3/1.
// 错误诊断函数
//

#ifndef LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H
#define LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H


#ifdef __GNUC__
#define NORETURN __attribute__ ((__noreturn__))
#else
#define NORETURN
#endif // __GNUC__


void errExit(const char* format, ...) NORETURN;
void errExitEn(int err_num, const char* format, ...) NORETURN;
void fatal(const char* format, ...) NORETURN;
void usageErr(const char* format, ...) NORETURN;
void cmdLineErr(const char* format, ...) NORETURN;

#endif //LINUX_PROGRAMMING_INTERFACE_ERROR_FUNCTION_H
