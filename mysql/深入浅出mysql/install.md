```bash
# 查看系统信息
$ cat /etc/issue
Ubuntu 18.04.1 LTS \n \l
$ uname -a
Linux ljs 4.15.0-52-generic #56-Ubuntu SMP Tue Jun 4 22:49:08 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux


# install mysql
$ sudo apt-get update
$ sudo apt-get install mysql-server
# 初始化配置, 设置root密码等
$ sudo mysql_secure_installation
# 查看服务状态
$ systemctl status mysql
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2019-07-04 20:46:02 CST; 3min 40s ago
 Main PID: 31875 (mysqld)
    Tasks: 29 (limit: 4915)
   CGroup: /system.slice/mysql.service
           └─31875 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid

7月 04 20:46:02 ljs systemd[1]: Starting MySQL Community Server...
7月 04 20:46:02 ljs systemd[1]: Started MySQL Community Server.


# 开启mysql
$ systemctl start mysql
# 关闭mysql
$ systemctl stop mysql
# 设置mysql开机自启动
$ sudo update-rc.d mysql defaults


# remove mysql
# 方式1, 先列出与mysql相关的软件, 选择性删除
$ dpkg --list | grep -i mysql
$ sudo apt-get autoremove --purge mysql-×××
# 方式2 清除和mysql相关的所有软件
$ sudo apt-get autoremove --purge mysql-\*
```



root远程访问配置

```bash
mysql> use mysql;
mysql> update user set host='%' where user='root' AND host='localhost';
mysql> UPDATE user SET plugin="mysql_native_password", authentication_string=PASSWORD("password") WHERE user="root";
mysql> FLUSH PRIVILEGES;

mysql> SELECT user, host, plugin, authentication_string FROM user where user="root";
+------+------+-----------------------+-------------------------------------------+
| user | host | plugin                | authentication_string                     |
+------+------+-----------------------+-------------------------------------------+
| root | %    | mysql_native_password | *6C362347EBEAA7DF44F6D34884615A35095E80EB |
+------+------+-----------------------+-------------------------------------------+

```

