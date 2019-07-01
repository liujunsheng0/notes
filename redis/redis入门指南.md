redis：字典结构的存储服务器。

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
| databases        | 16                              | 默认的数据库数量                                             |
| maxmemory        | N bytes                         | 限制redis最大可用内存大小（单位是字节）                      |
| maxmemory-policy | volatile-ttl                    | 内存超过maxmemory后使用maxmemory-policy制定的策略来删除不需要的键，直至占用内存小于maxmemory |
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
|          |            |

