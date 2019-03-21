/*
 * 密码文件: /etc/passwd
 *      每行包含七个字段, 以: 分隔
 *      如 root:x:0:0:root:/root:/bin/bash
 *      登录名          一般为用户名
 *      经过加密的密码  如果启用了shadow密码, 该字段通常为字母x, 经过加密处理的密码存储在/etc/shadow中
 *                      如果该字段为空, 则该账户登录时无需密码
 *      用户id
 *      组id            第一次分配的组ID,用户与组之间的关系会存储在/etc/group中
 *      注释            关于用户的描述性文字
 *      主目录          用户登陆后所处的初始路径
 *      登录shell       用户登录后, 便交由该程序控制, 通常为bash
 *
 *  shadow密码文件: /etc/shadow
 *  密码放在/etc/shadow原因: 安全原因, 因为许多系统工具都需要读/etc/passwd的信息, 所以不得不将/etc/passwd的可读权限放开,
 *                           攻击者会采用枚举密码与加密后的密码对比, 从而破解密码.
 *  /etc/shadow是防范此类攻击的手段之一
 *
 * 组文件: /etc/group
 * 如 sudo:x:27:cmldc,lxy,jn,wcg,zxy,cmcm,zdd,lxx
 *      组名
 *      经过加密后的密码
 *      组id
 *      用户列表, 属于该组的用户名列表, 之间以逗号分隔
 */