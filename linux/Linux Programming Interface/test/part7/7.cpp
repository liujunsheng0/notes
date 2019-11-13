#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include "error_functions.h"
/*
 * 在堆上分配内存
 * 堆: 高地址 -> 低地址
 * program break: 堆的当前内存边界
 * 分配/释放内存, 其实就是命令内核改变进程的program break位置. 在program break位置抬升后, 程序就可以访问新分配区域内的
 *                任何地址.
 * 操纵program break的系统调用:
 *      int brk(void* end_data_segment); 成功:0, 失败:-1
 *          将program break设置为end_data_segment所指定的位置.
 *
 *      void *sbrk(intptr_t increment); 基于brk实现的
 *          返回(当前program break + increment)的地址
 *          sbrk(0): 返回program break的当前位置
 *
 *  C程序使用malloc. free在堆上分配和释放内存
 *      void *malloc(size_t size);成功: 返回申请内存的地址; 失败: NULL
 *          实现: 扫描空闲内存块列表, 如果找到了大于等于的空闲内存块, 返回给调用者, 并将剩余的空闲分区保留在空闲分区块中,
 *                空闲分区块中没有合适的, malloc会调用sbrk()分配比申请的内存更大的内存块大小, 减少对sbrk的调用, 并将
 *                空闲分区放至空闲分区表中
 *                (申请内存时, 不是以字节的倍数来申请的, 而是以虚拟内存页的倍数来申请的, 多出的部分放至空闲分区表)
 *
 *      void free(void *ptr); 释放ptr参数所指向的内存块
 *          一般情况下, free()并不会降低program break的位置, 而是将这块内存添加到空闲内存列表中, 供后续的malloc()使用
 *          原因: 1. 被释放的内存块通常位于堆的中间, 而非顶部, 因此降低program break是不可能的
 *                2. 最大限度减少了系统调用sbrk()的使用, 系统调用的开销虽小, 但是频繁调用也是费时的
 *                3. 大多数情况下, 降低program break的位置不会对那些大量分配内存的程序有多少帮助, 因为他们通常都是反复
 *                   释放和申请内存
 *          当堆顶空闲内存足够大的时候, free()才会电影sbrk来降低program break的地址, 一般为258kb
 *          当进程终止时, 其占用的所有内存都会返还给操作系统.
 */

void memory() {
    int buf_size = 1024;
    size_t block_size = 24;
    int step = 1;
    char *ptr[buf_size];

    printf("initial program break: %10p\n", sbrk(0));

    for (int i = 0; i < buf_size; i++) {
        ptr[i] = (char*)malloc(block_size);
        if(ptr[i] == NULL) {
            Exit("malloc error");
        }
    }

    printf("malloc %d bytes\n", buf_size * (int)block_size);
    printf("malloc  program break: %10p\n", sbrk(0));

    for (int i = 0; i < buf_size; i+=step) {
        free(ptr[i]);
    }

    printf("free    program break: %10p\n", sbrk(0));
}


int main(){
    memory();
    return 0;
}