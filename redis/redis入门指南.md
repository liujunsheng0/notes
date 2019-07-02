[官方文档](http://redisdoc.com/index.html)

[redis](http://redisdoc.com/index.html)：字典结构的存储服务器。

key：键名

value：键值

**NOTICE**

> + 所有redis命令都是原子操作
> + redis中的类型不支持嵌套，每个元素都只能是字符串类型

# 可执行文件

| redis-server    | redis服务器（启动redis服务） |
| --------------- | ---------------------------- |
| redis-cli       | redis命令行客户端            |
| redis-benchmark | redis性能测试工具            |
| redis-check-aof | AOF文件修复工具              |
| redis-check-dum | RDB文件检测工具              |
| redis-sentinel  | sentinel服务器               |



# 配置

配置文件路径

```bash
/etc/init.d/redis-server

# 配置redis随系统启动
update-rc.d redis-server defaults
```

参数	

| 配置名           | 值                              | 说明                                                         |
| ---------------- | ------------------------------- | ------------------------------------------------------------ |
| daemonize        | yes                             | 使redis以守护进程模式运行                                    |
| pidfile          | /var/run/redis/redis-server.pid | 设置redis的PID文件位置                                       |
| port             | 端口，默认为6379                | 设置redis监听的端口号                                        |
| dir              | /var/lib/redis                  | 设置持久化文件存放位置                                       |
| dbfilename       | dump.rdb                        | 快照文件名                                                   |
| databases        | 16                              | 默认的数据库数量                                             |
| maxmemory        | N bytes                         | 限制redis最大可用内存大小（单位是字节）                      |
| maxmemory-policy | volatile-ttl                    | 内存超过maxmemory后使用maxmemory-policy制定的策略来删除不需要的键，直至占用内存小于maxmemory |
| appendonly       | yes/no                          | 开启AOF持久化，默认不不开启                                  |
| appendfilename   | appendonly.aof                  | AOF持久化文件名                                              |
| host             | 默认为0.0.0.0                   | ip                                                           |
| requirepass      |                                 | 登录密码，默认无                                             |
|                  |                                 |                                                              |
|                  |                                 |                                                              |
|                  |                                 |                                                              |
|                  |                                 |                                                              |
|                  |                                 |                                                              |

maxmemory-policy可选值

| 规则            | 说明                                              |
| --------------- | ------------------------------------------------- |
| volatile-lru    | 使用LRU算法删除一个键，只对设置了过期时间的键生效 |
| allkeys-lru     | 使用LRU算法删除一个键                             |
| volatile-random | 随机删除一个键，只对设置了过期时间的键生效        |
| allkeys-radom   | 随机删除一个键                                    |
| volatile-ttl    | 删除过期时间最近的一个键                          |
| noevction       | 不删除键，返回错误                                |



# 多数据库

redis提供了多个多个用来存储数据的字典。客户端可以指定存在哪个字典中。

每个数据库都是以一个从0开始的递增数字命名，默认支持16个数据库。可通过databases来修改这一参数。默认连接名称为0的数据库。

```bash
# 切换数据库
select 0/1/2/3...
```

> redis不支持自定义数据库名
>
> redis也不支持为每个数据库设置不同的访问密码
>
> redis的不同数据库更像命名空间，不适合存储不同应用程序的数据
>
> 一个空的redis服务大概占用的内存为1MB左右



# 命令

**Notice**

+ redis命令不区分大小写，键名区分大小写

##　 获取符合规则的键名列表

```bash
KEYS PATTERN
```

通用符规则

| ?    | 匹配任意一个字符                               |
| ---- | ---------------------------------------------- |
| *    | 匹配任意个字符                                 |
| []   | 匹配括号间的任一字符，可以使用-指定范围如[a-d] |
| \x   | 用于转义字符，如需要匹配?，需要使用\?          |

> KEYS命令会遍历所有的键，键较多时影响性能，不建议在生产环境中使用

## 判断一个键是否存在

```bash
EXISTS key
# return 1 if exist else 0
```

## 删除键

```bash
DEL key [key...]
# return number of delete

DEL key1 key2 key3

# 删除以user开头的键
redis-cli KEYS "user*" | xargs redis-cli DEL 
```

> del 不支持通配符，可以结合管道批量删除

## 键值的类型

```bash
type key
```

+ string
+ hash（散列类型）
+ list（列表类型）
+ set（集合类型）
+ zset（有序集合类型）

## string

一个字符传类型键值允许存储数据的最大容量为521MB

```bash
# 设置键名-键值 
SET key value

# 获取, 如果不存在返回nil
GET key

# 递增数字, 键值为整数时, 让当前键递增, 返回递增后的值; 如果不存在时会默认键值为0, 所以返回1
# 当键值不为整数时, redis会提示错误（浮点数也会提示错误）
# incr = increment
INCR key

# 与INCR类似， 只不过可通过increment参数指定指定一次新增的值
# INCY key == INCRBY key 1
INCRBY key increment

# decrement 递减, 与INCR相反
DECR key
DECRBY key decrement

# 向尾部追加值，如果key不存在相当于SET key value
APPEND key value

# 获取字符串长度
STRLEN key

# 同时获取/设置多个键值
MGET key [key...]
MSET key value [key value...]

# 位操作
# 获取字符串指定bit位置的值(0/1), 如果越界/key不存在返回0
GETBIT key offset
# 设置指定key的offset位的值, 如果offset越界/key不存在补全0
SETBIT key offset value
# 统计二进制中1的个数，start：字节位置, end：结束位置（包含）
BITCOUNT key [start] [end]
# 多个key进行位运算, 结果存储在destkey, operation可选值为AND OR XOR NOT
BITOP operation destkey key [key...]
#　如set a bar，ascii码为 98，97,114
#             b         a          f
# 二进制： 0110 0010 0110 0001  0111 0010
# index:  0123 4567 89...
```

## hash（散列类型）

redis采用字典结构以键值对的形式存储数据，而散列类型的键值也是一种字典结构，其存储了字段和字段值的映射，**但字段值只能是字符串，不能是其他类型。**也就是说散列类型不支持类型嵌套。一个散列类型键可以包含`2^32-1`个字段

```bash
# 不区分插入和更新操作，插入操作返回1，更新操作返回0
HSET key fiedl value
# 获取值
HGET key field
HMSET key field value [field value...]
HMGET key field [field...]
# 获取全部的field，返回结果为字段和字段值组成的列表
HGETALL key

# 判断字段是否存在，存在返回1，不存在返回0
HEXISTS key field

# 当字段不存在时赋值，NX = IF NOT EXIST
HSETNX key field value

# 增加数字, 用法通INCRBY
HINCRBY key field increment

# 删除
HDEL key field [field...]

# 只获取字段名/字段值
HKEYS key
HVALUE key
# 获取字段数量
HLEN key
```

## list（列表类型）

存储一个有序的字符串列表。内部实现为双向链表，所以向两端添加元素时间复杂度为O(1)，但是通过索引访问元素较慢。

```bash
# L = LEFT R = RIGHT，向列表两端增加元素，返回增加元素后列表的长度
LPUSH key value [value]
RPUSH key value [value]

# 两端弹出元素
LPOP key
RPOP key

# 获取列表中元素个数，key不存在时返回0
LLEN key

# 获取列表片, [start, stop], 索引从0开始，支持负索引，如-1代表最右边的元素
LRANGE key start stop

# REM=REMOVE，删除列表中前count个值为value的元素，return实际删除的元素个数
# count > 0, 从左开始删除
# count < 0, 从右开始删除
# count = 0，删除所有置为value的元素
LREM key count value

# index支持负索引， 如果越界/key不存在会提示错误
LINDEX key index
LSET key index value

# 删除指定范围之外的元素，保留[start, end]的元素
LTRIM key start end

# 插入元素，如果不存在pivot的话，则不做插入操作，return key的元素个数
LINSERT key BEFORE/AFTER pivot value

# RPOP source -> LPUSH destination
RPOPLPUSH source destination
```

## set（集合）

```bash
# 新增
SADD key member [member...]
# 删除， SET REMOVE
SREM key member [member...]
# 获取全部
SMEMBERS key
# 判断是否在集合中
SISMEMBER key member
# 集合操作
SDIFF key [key...]  # 差集
SINTER key [key...] # 交集
SUNION key [key...] # 并集
# 获取个数
SCARD key
# 随机获取集合中的count个元素
SRANDMEMBER key count
# 随机弹出一个元素
SPOP key
```

## sorted set（有序集合类型）

在集合的基础上有序集合类型为集合中的每个元素都关联了一个分数。

有序集合是通过散列表和跳跃表实现的

```bash
# 新增元素
ZADD key score member [score member...]

#　获取元素的分数，如果不存在返回nil
ZSCORE key member

# 获得排名在某个范围的元素列表, [start, stop]，支持负索引
# 无WITHSCORES返回[元素1, 元素2...]; 有WITHSCORES会连分数一起返回[元素1, 分数1，元素2, 分数2...]
# ZRANGE 从小到大，ZREVRANGE 从大到小
ZRANGE key start stop [WITHSCORES]
ZREVRANGE key start stop [WITHSCORES]

# 增加某个元素的分数，返回更改后的分数，如果不存在会提示错误
ZINCRBY key member score

# 获取元素个数
ZCARD key
# 获取分数在[min, max]的元素个数
ZCOUNT key min max
# 删除, 返回删除的数量
ZREM key member [member]

# 获取排名，从0开始，不存在返回nil
ZRANK key member
ZREVRANK key member

# 删除分数范围[min, max]的所有元素
ZREMRANGEBYSCORE key min max
```

# 事务

定义：一组命令的集合。

事务同命令一样都是redis的最小执行单位，一个事务中的命令要么都执行，要么都不执行。

原理：先将一个事务的命令发送给redis，然后再让redis依次执行这些命令。

格式：

```bash
$ MULTI         # 告诉redis下面的命令属于同一个事务，暂时不要执行，先保存起来
OK
$ LPUSH list 1
QUEUED          # 命令已经进入等待执行的事务队列中
$ LPUSH list 2
QUEUED          # 命令已经进入等待执行的事务队列中
$ ...
$ EXEC          # 依次执行事务队列中的所有命令
1) (integer) 1  # EXEC的返回值就是这些命令返回值组成的列表，返回值顺序和命令的顺序相同
2) (integer) 2
```

> + redis保证一个事务中的所有命令要么都执行，要么都不执行。如果在发送EXEC命令前客户端断线了，则redis会清空事务队列，事务中的命令都不执行。一旦客户端发送了EXEC命令，所有的命令都会执行，客户端断线也没关系，因为redis中记录了要执行的命令
>
> + redis的事务并没有提供回滚功能

## 错误处理

+ 事务中出现语法错误，如

  ```bash
  $ MULTI
  ok
  $ SET a
  (error) ERR number of arguments for set command
  $ ERRORCOMMAND key
  (error) unknown command ERRORCOMMAND
  $ EXEC
  (error) EXECABORT Transaction discarded because of previous errors.
  ```

  redis会直接返回错误，不会执行命令

+ 运行错误

  命令执行时出现的错误，如用散列类型的命令操作集合类型的键。这种错误在实际执行前是无法发现的，所以在事务里这样的命令是被redis接受并执行的。如果事务里的一条命令出现了错误，事务里其他的命令依然会继续执行（包括出错命令之后的命令）。

  ```bash
  $ MULTI
  ok
  $ SET key value
  QUNUED
  $ SADD key a
  QUNUED
  $ SET key1 value1
  QUNUED
  $ EXEC
  1) OK
  2) (error) WRONGTYPE Operation against a key holding the wrong kind of value 
  3) OK
  ```

# WATCH

WATCH：监控一个或多个键，一旦其中有一个键被修改或删除，之后的事务就不会执行。监控一直持续到EXEC命令。

UNWATCH：取消监控

```bash
$ set key 1
OK
$ watch key
OK
# 事务执行行修改了key的值，所以事务中的set key 3并没有执行，EXEC返回空结果
$ set key 2 
OK
$ MULTI
OK
$ set key 3
QUEUED
$ exec
(nil)
$ get key
"2"

# 利用watch 实现INCR
def INCR(key):
	WATCH key
	value = GET key + 1
	# key的值中途改变的话，事务不会执行
	MULTI
		set key value
	result = EXEC
	return result[0]
```

> WATCH命令只是当被监控的键被修改后阻止之后一个事务的执行，而不能保证其他客户端不修改这一键值。
>
> 执行EXEC命令后会取消对所有键的监控
>
> 如果使用WATCH监测一个拥有过期时间的键，该键时间到期后自动删除并不会被WATCH命令认为该键被改变

# 过期时间

```bash
# 设置key的过期时间，seconds=剩余秒数，到期后redis会自动删除它
EXPIRE key seconds
PEXPIRE key millisecond 
# return 1 if set success，0 if key not exist or set fail

# 返回过期剩余时间
TTL key
# return 
# 	-2: 键不存在
# 	-1: 存在但是无过期时间
#    剩余秒数: 正常

# 取消过期时间的设置
PERSIST key
# RETURN 1 if success，否则返回（键不存在/键本来就是永久的）
```

用处：

+ 实现访问频率限制
+ 缓存

# 持久化

RDB：根据指定的规则"定时"将内存中的数据存储在硬盘上

AOF：后者在每次执行命令后将命令本身记录下来

两种持久化方式可以单独使用其中一种,但更多情况下是将二者结合使用

## RDB

RDB方式的持久化是通过快照(snapshotting)完成的，当符合一定条件时redis会自动将
内存中的所有数据生成一份副本并存储在硬盘上，这个过程即为“快照”。

redis会在以下几种情况下对数据进行快照：

+ 根据配置规则进行自动快照
+ 用户执行 SAVE或 BGSAVE命令
+ 执行 FLUSHALL命令
+ 执行复制(replication)时 

### 根据配置规则进行自动快照

redis允许用户自定义快照条件，当符合快照条件时，redis会自动执行快照操作。进行
快照的条件可以由用户在配置文件中自定义，由两个参数构成：时间窗口M和改动的键的个
数N。每当时间M内被更改的键的个数大于N时，符合自动快照条件。

可在redis配置文件中预设进行快照的条件，条件之间是或的关系

```bash
save 900 1     # 900秒内有>=1    个键被修改则进行快照
save 300 10    # 300秒内有>=10   个键被修改则进行快照
save 60 10000  # 60 秒内有>=10000个键被修改则进行快照
```

### 用户执行 SAVE或 BGSAVE命令

SAVE：redis同步执行快照，阻塞客户端请求。生产环境中避免使用

BGSAVE：后台异步进行快照，同时还可以响应来自客户端的请求。执行BGSAVE后立即返回ok，如果想知道快照是否完成，可以通过 LASTSAVE命令获取最近一次成功执行快照的时间，返回结果是一个Unix时间戳

> 手动快照时，推荐使用BGSAVE（background save）
>
> 自动快照时使用的策略就是异步快照

### 执行 FLUSHALL命令

当执行 FLUSHALL 命令时，Redis 会清除数据库中的所有数据。

**不论清空数据库的过程是否触发了自动快照条件，只要自动快照条件不为空redis就会执行一次快照操作。**例如，当定义的快照条件为当1秒内修改10 000个键时进行自动快照，而当数据库里
只有一个键时，执行FLUSHALL命令也会触发快照，即使这一过程实际上只有一个键被修改了。当没有定义自动快照条件时,执行FLUSHALL则不会进行快照。

### 执行复制(replication)时

当设置了主从模式时,Redis 会在复制初始化时进行自动快照。

###　快照原理

Redis默认会将快照文件存储在Redis当前进程的工作目录中的dump.rdb文件中，可以通过配置dir和dbfilename两个参数分别指定快照文件的存储路径和文件名。

**快照的过程如下**

+ redis使用fork函数复制一份当前进程(父进程)的副本(子进程)
+ 父进程继续接收并处理客户端发来的命令，而子进程开始将内存中的数据写入硬盘中的临时文件
+ 当子进程写入完所有数据后会用该临时文件替换旧的 RDB 文件,至此一次快照操作完成

​        在执行 fork 的时候操作系统会使用写时复制(copy -on-write)策略，即fork函数发生的一刻父子进程共享同一内存数据，当父进程要更改其中某片数据时(如执行一个写命令)，操作系统会将该片数据复制一份以保证子进程的数据不受影响，所以新的RDB文件存储的是执行fork一刻的内存数据。

​	写时复制策略也保证了在 fork 的时刻虽然看上去生成了两份内存副本，但实际上内存的占用量并不会增加一倍。这就意味着当系统内存只有2 GB，而Redis数据库的内存有1.5 GB时，执行 fork后内存使用量并不会增加到3GB。
	当进行快照的过程中，如果写入操作较多，造成 fork 前后数据差异较大，是会使得内存使用量显著超过实际数据大小的，因为内存中不仅保存了当前的数据库数据，而且还保存着 fork 时刻的内存数据。进行内存用量估算时很容易忽略这一问题,造成内存用量超限。
	redis在进行快照的过程中不会修改RDB文件，只有快照结束后才会将旧的文件替换成新的，也就是说任何时候 RDB 文件都是完整的。RDB 文件是经过压缩(可以配置rdbcompression 参数以禁用压缩节省CPU占用)的二进制格式，占用的空间会小于内存中的数据大小，更加利于传输。
	redis启动后会读取RDB快照文件，将数据从硬盘载入到内存。根据数据量大小与结构和服务器性能不同，这个时间也不同。通常将一个记录1000万个字符串类型键、大小为1GB的快照文件载入到内存中需要花费20~30秒。
	通过RDB方式实现持久化，一旦Redis异常退出,就会丢失最后一次快照以后更改的所有
数据。这就需要开发者根据具体的应用场合，通过组合设置自动快照条件的方式来将可能发
生的数据损失控制在能够接受的范围。**如果数据相对重要，则可以使用AOF方式进行持久化。**

## AOF

​	当使用redis存储非临时数据时，一般需要打开AOF持久化来降低进程中止导致的数据丢
失。AOF可以将redis执行的每一条写命令追加到硬盘文件中，这一过程显然会降低redis 的
性能，但是大部分情况下这个影响是可以接受的。

​	默认情况下redis没有开启**AOF(Append Only File)**方式的持久化，可以通过 appendonly
参数启用：`appendonly yes`。

​	开启AOF持久化后每执行一条会更改redis中的数据的命令，Redis就会将该命令写入硬盘中的AOF文件。AOF文件的保存位置和RDB文件的位置相同，都是通过dir参数设置的，默认的文件名是appendonly.aof，可以通过appendfilename参数修改`appendfilename appendonly.aof`

### AOF的实现

**AOF文件以纯文本的形式记录了redis执行的写命令**。每当达到一定条件时redis就会自动重写AOF文件，覆盖掉无用的写命令。

可在配置文件中指定触发条件

```bash
#　当前的AOF文件大小超过上一次重写时的AOF文件大小的百分之多少时会再次进行重写　 
auto-aof-rewrite-percentage 100
# 限制了允许重写的最小AOF文件大小
auto-aof-rewrite-min-size 64mb
```

可以使用BGREWRITEAOF手动执行AOF文件重写。

虽然每次执行更改数据库内容的操作时，AOF都会将命令记录在AOF文件中，但是事实上由于操作系统的缓存机制，数据并没有真正地写入硬盘，而是进入了系统的硬盘缓存。在默认情况下系统每30秒会执行一次同步操作，以便将硬盘缓存中的内容真正地写入硬盘，在这30秒的过程中如果系统异常退出则会导致硬盘缓存中的数据丢失。一般来讲启用AOF持久化的应用都无法容忍这样的损失，这就需要Redis在写入AOF文件后主动要求系统将缓存内容同步到硬盘中。在 Redis 中我们可以通过 appendfsync 参数设置同步的时机

```bash
# always表示每次执行写入都会执行同步,这是最安全也是最慢的方式
appendfsync always

# 每秒执行一次同步操作
appendfsync everysec

# 不主动进行同步操作,而是完全交由操作系统来做(即每30秒一次),这是最快但最不安全的方式（默认）
appendfsync no
```

redis 允许同时开启 AOF 和 RDB，既保证了数据安全又使得进行备份等操作十分容易。此时重新启动Redis后Redis会使用AOF文件来恢复数据，因为AOF方式的持久化可能丢失的数据更少。



#　安全

redis的安全设计是在**redis运行在可信环境**这个前提下做出的。

在生产环境运行时不能允许外界直接连接到 Redis 服务器上，而应该通过应用程序进行中转，运行在可信的环境中是保证redis安全的最重要方法。

redis的默认配置会接受来自任何地址发送来的请求，即在任何一个拥有公网IP的服务器上启动 redis 服务器，都可以被外界直接访问到。要更改这一设置，在配置文件中修改bind参数，如只允许本机应用连接Redis，可以将bind参数改成`bind 127.0.0.1`
bind参数只能绑定一个地址，如果想更自由地设置访问规则需要通过防火墙来完成。

# 简拼

| cli   | client command line interface |
| ----- | ----------------------------- |
| redis | remote dictionary server      |
| INCR  | increment 增加，增长          |
| DECR  | decrment 减少                 |
| TTL   | Time To Live                  |
|       |                               |
|       |                               |
|       |                               |
|       |                               |
|       |                               |



# 单词

| sentinel | 哨兵       |
| -------- | ---------- |
| expire   | 到期       |
| persist  | 坚持，保持 |
| cluster  | 集群       |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |
|          |            |

