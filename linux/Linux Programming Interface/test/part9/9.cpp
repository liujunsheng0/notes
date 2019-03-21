/*
 * 进程凭证
 * 每一个进程都有一套用数字表示的用户ID(UID)和组ID(GID), 有时, 也将这些ID称之为进程凭证, 具体如下
 *      实际用户ID(real user ID)和实际组ID(read group ID)
 *      有效用户ID(effective user ID)和有效组ID(effective group ID)
 *      保存的set-user-ID和保存的set-group-ID
 *      文件系统用户ID(file-system user ID)和文件系统组ID(file-system group ID)(Linux 专有)
 *      辅助组ID
 *
 * 实际用户ID(real user ID)和实际组ID(read group ID)
 *      确定了进程所属的用户和组, 登录时从/etc/passwd中读取的第三, 四个字段, 置为实际用户ID和组ID.
 *      创建新进程时, 从父进继承这些ID
 *
 * 有效用户ID(effective user ID)和有效组ID(effective group ID)
 *      进程对诸如文件之类资源的访问, 其访问权限由有效ID决定.
 *      当进程尝试执行各种系统调用时, 将结合有效用户ID, 有效组ID, 辅助组ID来确定授予进程的权限.
 *      通常情况下, 有效用户ID和组ID与其相应的实际ID相等
 *
 * set-user-ID和set-group-ID程序
 *      set-user-ID程序会将进程的有效用户ID置为可执行文件的用户ID(属主), 从而获得常规情况下并不具有的权限.
 *      如果文件设置了set-user-ID和set-group-ID, 那么通常用来表示文件可执行的x标识会被s所替换
 *      如: ls -l main
 *              -rwxr-xr-x 1 root root .....
 *          chmod u+s main
 *          chmod g+s main
 *          ls -l main
 *              -rwsr-sr-x 1 root root .....
 *          当运行文件时, 内核会将有效用户ID和有效组ID设置为可执行文件的用户ID和组ID, 通过这种方法修改进程的有效用户ID
 *          或者组ID, 能使进程获得常规情况下所不具有的权限.
 *          当一个可执行文件的属主为root, 并未此程序设置了set-user-ID权限位, 那么当运行该程序时, 进程会获得root权限
 *     使用demo: passwd, mount, umount, su等命令
 *
 * 文件系统用户ID(file-system user ID)和文件系统组ID(file-system group ID)(Linux 专有)
 *      在Linux系统中, 要进行诸如打开文件, 改变文件属主. 修改文件权限之类的文件系统操作时, 决定其操作操作权限的是文件
 *      系统用户ID和组ID,
 *      通常文件系统ID和组ID的值等于相应的有效用户ID和组ID, 只要有效用户或组ID发生了变化, 则相应的文件系统ID也会随之变化
 *
 *
 * 辅助组ID
 *      用于标识进程所属的若干附加的组.
 */

/*
 * 获取进程凭证
 *      可利用Linux特有的/proc/PID/status文件, 通过对其中Uid, Gid, Groups各行信息的检查来获取进程的凭证.
 *      Uid和Gid各行, 按实际, 有效, 保存设置和文件系统ID的顺序来展示相应表示符.
 *
 * 总结:
 *      在大多数UNIX实现中, 进程对诸如文件之类资源的访问, 其访问权限由有效ID决定, 然而, Linux系统会使用文件系统ID来决定
 *      对文件的访问权限, 而将有效ID用户检查其他权限.
 */