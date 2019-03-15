/*
 * 多个文件描述符可指向同一打开文件, 这些文件描述符可在相同或不同的进程中打开
 *
 * 要理解文件描述符和打开文件之间的关系, 需要查看内核维护的三个数据结构:
 *     1. 进程级的文件描述符表
 *     2. 系统级的打开文件表
 *     3. 文件系统的i-node表
 *
 *  进程级的文件描述符表, 针对每个进程, 内核为其维护打开文件的描述符表. 记录了文件描述符相关信息
 *      1. 控制文件描述符操作的一组标志
 *      2. 对打开文件句柄的引用
 *
 *  系统级的打开文件表, 内核对所有打开的文件维护一个系统级的描述表格（打开文件表）, 表中的内容为打开文件句柄(open file handle).
 *  文件句柄存储了与打开文件相关的全部信息, 如
 *      1. 当前文件偏移量
 *      2. 打开文件时使用的状态标志, 即open()的flags参数
 *      3. 文件访问模式， 即open()的flags参数中的只读, 只写, 读写模式中的一个
 *      4. 与信号驱动I/O相关的设置
 *      5. 对该文件i-node对象的引用
 *
 *  i-node表
 *      1. 文件类型和访问权限
 *      2. 一个指针, 指向该文件所持有的锁的列表
 *      3. 文件的各种属性, 包括文件大小, 修改时间等
 *
 *  由file_and_file_descriptor.png可知, 文件描述符类似于数组中的下标
 *
 *  https://juejin.im/entry/5b56f9045188251b157bb645
 *  https://www.cnblogs.com/Orgliny/articles/5699479.html
 *  同一进程的文件描述符指向了同一个打开的文件句柄: 可能是通过调用dup(), dup2() 或 fcntl形成的
 *  不同进程文件描述符指向了同一个打开的文件句柄: fork() 不同进程为父子关系或者通过套接字将打开的文件描述法传递
 *  两个不同的文件描述符, 若指向了同一文件句柄, 将共享同一文件偏移量.
 *  (相同进程多次打开同一文件时, 句柄是不同的.)
 *  文件描述符标志位进程和文件描述符私有, 对这一标志的修改不会影响同一进程或不同进程中的其他描述符
 *
 *  /dev/stdin,  /dev/fd/0对应的标准输入
 *  /dev/stdout, /dev/fd/1对应的标准输出
 *  /dev/stderr, /dev/fd/2对应的标准错误
 *  /proc/进程号/fd/n n是进程中打开的文件对应的文件描述符
 *  查看进程打开的文件数量: ls -l /proc/进程号/fd | wc -l (同一个文件, 多次打开, 文件句柄是不一样的)
 *
 *  文件相关系统调用

 *  open(...)
 *  read(...)
 *  write(...)
 *  lseek(...)
 *  close(...)
 *
 *  pread(int fd, void* buf, size_t count, off_t offset); 在指定的offset处进行读写，而且不会改变偏移量
 *  pwrite(int fd, void* buf, size_t count, off_t offset);
 *
 *  ssize_t readv(int fd, const struct iovec *iov, int iovcnt);  批量读取/写入
 *  ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
 *
 *  ssize_t preadv(int fd, const struct iovec *iov, int iovcnt);  指定offset处, 批量读取/写入
 *  ssize_t pwritev(int fd, const struct iovec *iov, int iovcnt);
 *
 *  若当前文件大于参数length, 丢弃超出的部分, 小于length, 调用将添加空字节或者一个文件空洞
 *  int truncate(const char* filename, off_t length);
 *  若当前文件大于参数length, 丢弃超出的部分, 小于length, 调用将添加空字节或者一个文件空洞或者返回错误
 *  int ftruncate(int fd, off_t length);
 */