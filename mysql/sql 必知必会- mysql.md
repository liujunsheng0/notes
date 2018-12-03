# 数据库

```mysql
# 查看有哪些数据库
SHOW DATABASES;
# 创建数据库test
CREATE DATABASE test;
# 删除test
DROP DATABASE test;
# 将test设置为默认数据库
USE test;
```

# 表

```mysql
# 复制一张表的结构
CREATE TABLE test_copy LIKE test;
# 删除表
DROP TABLE table;
# 重命名表
RENAME TABLE test TO test_rename;

# 更新表使用 ALTER TABLE
# 修改表名
ALTER TABLE t_book RENAME TO bbb;
# 添加列
ALTER TABLE 表名 ADD COLUMN 列名 varchar(30);
# 删除列
ALTER TABLE 表名 DROP COLUMN 列名;
# 修改列名
ALTER TABLE 表名 CHANGE old_name new_name int;
```



## [创建表][1]

```mysql
-- -----------------------------------------
-- Sams Teach Yourself SQL in 10 Minutes
-- http://forta.com/books/0672336073/
-- Example table creation scripts for MySQL.
-- -----------------------------------------
-- ----------------------
-- Create Customers table
-- ----------------------
CREATE TABLE Customers
(
  cust_id      char(10)  NOT NULL COMMENT '唯一的顾客ID',
  cust_name    char(50)  NOT NULL COMMENT '顾客公司名',
  cust_address char(50)  NULL COMMENT '顾客的地址',
  cust_city    char(50)  NULL DEFAULT 'us' COMMENT '顾客所在国家',
  cust_state   char(5)   NULL COMMENT '顾客所在州',
  cust_zip     char(10)  NULL COMMENT '顾客地址邮政编码',
  cust_country char(50)  NULL COMMENT '顾客所在国家',
  cust_contact char(50)  NULL COMMENT '顾客名',
  cust_email   char(255) NULL COMMENT '顾客邮编'
);

-- -----------------------
-- Create OrderItems table
-- -----------------------
CREATE TABLE OrderItems
(
  order_num  int          NOT NULL COMMENT '订单号',
  order_item int          NOT NULL COMMENT '订单产品号（订单内的产品顺序）',
  prod_id    char(10)     NOT NULL COMMENT '产品id',
  quantity   int          NOT NULL COMMENT '物品数量',
  item_price decimal(8,2) NOT NULL COMMENT '物品价格'
);


-- -------------------
-- Create Orders table
-- -------------------
CREATE TABLE Orders
(
  order_num  int      NOT NULL COMMENT '唯一的订单号',
  order_date datetime NOT NULL COMMENT '订单日期',
  cust_id    char(10) NOT NULL COMMENT '订单顾客ID（关联到Customers表的cust_id)'
);

-- ---------------------
-- Create Products table
-- ---------------------
CREATE TABLE Products
(
  prod_id    char(10)      NOT NULL COMMENT '唯一的产品ID',
  vend_id    char(10)      NOT NULL COMMENT '产品供应商ID（关联到Vendors表的vend_id）',
  prod_name  char(255)     NOT NULL COMMENT '产品名',
  prod_price decimal(8,2)  NOT NULL COMMENT '产品价格',
  prod_desc  text          NULL COMMENT '产品描述'
);

-- --------------------
-- Create Vendors table
-- --------------------
CREATE TABLE Vendors
(
  vend_id      char(10) NOT NULL COMMENT '唯一的供应商ID',
  vend_name    char(50) NOT NULL COMMENT '供应商的名字',
  vend_address char(50) NULL COMMENT '供应商的地址',
  vend_city    char(50) NULL COMMENT '供应商所在的城市',
  vend_state   char(5)  NULL COMMENT '供应商所在州',
  vend_zip     char(10) NULL COMMENT '供应商地址的邮政编码',
  vend_country char(50) NULL COMMENT '供应商所在国家'
);


-- -------------------
-- Define primary keys
-- -------------------
ALTER TABLE Customers ADD PRIMARY KEY (cust_id);
ALTER TABLE OrderItems ADD PRIMARY KEY (order_num, order_item);
ALTER TABLE Orders ADD PRIMARY KEY (order_num);
ALTER TABLE Products ADD PRIMARY KEY (prod_id);
ALTER TABLE Vendors ADD PRIMARY KEY (vend_id);


-- -------------------
-- Define foreign keys(外键)
-- -------------------
ALTER TABLE OrderItems ADD CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (order_num) REFERENCES Orders (order_num);
ALTER TABLE OrderItems ADD CONSTRAINT FK_OrderItems_Products FOREIGN KEY (prod_id) REFERENCES Products (prod_id);
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers FOREIGN KEY (cust_id) REFERENCES Customers (cust_id);
ALTER TABLE Products ADD CONSTRAINT FK_Products_Vendors FOREIGN KEY (vend_id) REFERENCES Vendors (vend_id);
```

## [插入数据][1]

```mysql
-- -------------------------------------------
-- Sams Teach Yourself SQL in 10 Minutes
-- http://forta.com/books/0672336073/
-- Example table population scripts for MySQL.
-- -------------------------------------------


-- ------------------------
-- Populate Customers table
-- ------------------------
INSERT INTO Customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
VALUES('1000000001', 'Village Toys', '200 Maple Lane', 'Detroit', 'MI', '44444', 'USA', 'John Smith', 'sales@villagetoys.com');
INSERT INTO Customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact)
VALUES('1000000002', 'Kids Place', '333 South Lake Drive', 'Columbus', 'OH', '43333', 'USA', 'Michelle Green');
INSERT INTO Customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
VALUES('1000000003', 'Fun4All', '1 Sunny Place', 'Muncie', 'IN', '42222', 'USA', 'Jim Jones', 'jjones@fun4all.com');
INSERT INTO Customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
VALUES('1000000004', 'Fun4All', '829 Riverside Drive', 'Phoenix', 'AZ', '88888', 'USA', 'Denise L. Stephens', 'dstephens@fun4all.com');
INSERT INTO Customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact)
VALUES('1000000005', 'The Toy Store', '4545 53rd Street', 'Chicago', 'IL', '54545', 'USA', 'Kim Howard');

-- ----------------------
-- Populate Vendors table
-- ----------------------
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('BRS01','Bears R Us','123 Main Street','Bear Town','MI','44444', 'USA');
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('BRE02','Bear Emporium','500 Park Street','Anytown','OH','44333', 'USA');
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('DLL01','Doll House Inc.','555 High Street','Dollsville','CA','99999', 'USA');
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('FRB01','Furball Inc.','1000 5th Avenue','New York','NY','11111', 'USA');
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('FNG01','Fun and Games','42 Galaxy Road','London', NULL,'N16 6PS', 'England');
INSERT INTO Vendors(vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country)
VALUES('JTS01','Jouets et ours','1 Rue Amusement','Paris', NULL,'45678', 'France');

-- -----------------------
-- Populate Products table
-- -----------------------
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BR01', 'BRS01', '8 inch teddy bear', 5.99, '8 inch teddy bear, comes with cap and jacket');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BR02', 'BRS01', '12 inch teddy bear', 8.99, '12 inch teddy bear, comes with cap and jacket');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BR03', 'BRS01', '18 inch teddy bear', 11.99, '18 inch teddy bear, comes with cap and jacket');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BNBG01', 'DLL01', 'Fish bean bag toy', 3.49, 'Fish bean bag toy, complete with bean bag worms with which to feed it');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BNBG02', 'DLL01', 'Bird bean bag toy', 3.49, 'Bird bean bag toy, eggs are not included');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('BNBG03', 'DLL01', 'Rabbit bean bag toy', 3.49, 'Rabbit bean bag toy, comes with bean bag carrots');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('RGAN01', 'DLL01', 'Raggedy Ann', 4.99, '18 inch Raggedy Ann doll');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('RYL01', 'FNG01', 'King doll', 9.49, '12 inch king doll with royal garments and crown');
INSERT INTO Products(prod_id, vend_id, prod_name, prod_price, prod_desc)
VALUES('RYL02', 'FNG01', 'Queen doll', 9.49, '12 inch queen doll with royal garments and crown');

-- ---------------------
-- Populate Orders table
-- ---------------------
INSERT INTO Orders(order_num, order_date, cust_id)
VALUES(20005, '2012-05-01', '1000000001');
INSERT INTO Orders(order_num, order_date, cust_id)
VALUES(20006, '2012-01-12', '1000000003');
INSERT INTO Orders(order_num, order_date, cust_id)
VALUES(20007, '2012-01-30', '1000000004');
INSERT INTO Orders(order_num, order_date, cust_id)
VALUES(20008, '2012-02-03', '1000000005');
INSERT INTO Orders(order_num, order_date, cust_id)
VALUES(20009, '2012-02-08', '1000000001');

-- -------------------------
-- Populate OrderItems table
-- -------------------------
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20005, 1, 'BR01', 100, 5.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20005, 2, 'BR03', 100, 10.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20006, 1, 'BR01', 20, 5.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20006, 2, 'BR02', 10, 8.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20006, 3, 'BR03', 10, 11.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20007, 1, 'BR03', 50, 11.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20007, 2, 'BNBG01', 100, 2.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20007, 3, 'BNBG02', 100, 2.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20007, 4, 'BNBG03', 100, 2.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20007, 5, 'RGAN01', 50, 4.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20008, 1, 'RGAN01', 5, 4.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20008, 2, 'BR03', 5, 11.99);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20008, 3, 'BNBG01', 10, 3.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20008, 4, 'BNBG02', 10, 3.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20008, 5, 'BNBG03', 10, 3.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20009, 1, 'BNBG01', 250, 2.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20009, 2, 'BNBG02', 250, 2.49);
INSERT INTO OrderItems(order_num, order_item, prod_id, quantity, item_price)
VALUES(20009, 3, 'BNBG03', 250, 2.49);
```

## 查询

### 注释

```mysql
-- 这是注释, "--"之后的内容就是注释
```

### select

```mysql
# 所有列
SELECT * FROM Customers;
# 检索单列
SELECT cust_name FROM Customers;
# 多列需以 "," 分隔 
SELECT cust_name, cust_city, cust_address FROM Customers;
```

### DISTINCT

```mysql
# 仅需要不同的值, DISTINCT作用于所有列, 并不是跟在其后面的那一列 
# cust_country不同的行
SELECT DISTINCT cust_country FROM Customers;
# cust_country, cust_id 不同的行
SELECT DISTINCT cust_country, cust_id FROM Customers;
```

### LIMIT

限制返回的最大行数

```mysql
# 返回0,1行
SELECT cust_name FROM Customers LIMIT 2;
# 返回3,4行, OFFSET是指从哪行开始, 行数从0开始
SELECT cust_name FROM Customers LIMIT 2 OFFSET 3;
# LIMIT 2 OFFSET 3的简写
SELECT cust_name FROM Customers LIMIT 3, 2;
```

### ORDER BY

排序

> 使用ORDER BY时，需要放在select 语句的最后一条子句中
>
> 按多列排序时，需要安装指定的排序规则排序，如以下例子中，先按cust_id排列，如果cust_id相同，在根据cust_name排序

```mysql
SELECT * FROM Customers ORDER BY cust_id, cust_name;
```

排序方向

ASC 升序（默认），DESC降序

> DESTC只应用于其前面的列
>
> ASC：ASCENDING
>
> DESC：DESCENDING

```mysql
# 先按照cust_name降序排序, 如果cust_name名字相同,按cust_id升序排序
SELECT * FROM Customers ORDER BY cust_name DESC, cust_id;
```

###WHERE

指定搜索条件

```mysql
select * from table WHERE (condition1 AND condition2) OR (condition3)....
```

```mysql
SELECT prod_name, prod_price FROM Products where prod_price > 3;
SELECT prod_name, prod_price FROM Products where prod_price > 3 AND prod_price < 10;
SELECT prod_name, prod_price FROM Products where prod_price > 10 OR prod_price < 4;
SELECT prod_name, prod_price FROM Products where prod_price IN (3.49, 11.99);
SELECT prod_name, prod_price FROM Products where prod_price NOT IN (3.49, 11.99);
```

| 操作符      | 说明                 |
| ----------- | -------------------- |
| =           | 等于                 |
| <=          | 小于等于             |
| <           | 小于                 |
| >           | 大于                 |
| >=          | 大于等于             |
| !=          | 不等于               |
| BETWEEN  a  | 在a和b之间，包含a和b |
| IS NULL     | 为NULL               |
| IS NOT NULL | 不是NULL             |
| IN          | 指定符合条件的值     |
| NOT         | 否定后面的条件       |

> 当使用> < 等操作符时，不会将NULL包含其中，如搜索a < 1的行，不会将a=NULL的行包含其中
>
> AND，OR，IN 等可以组合使用，如果多个条件注意使用()，防止歧义

### LIKE

搜索，仅适用于文本字段，比较耗时

| 通配符 |                                                              |
| ------ | ------------------------------------------------------------ |
| %      | 表示任何字符出现任意次数，类似正则表达式中的" .* "，不会匹配值为NULL的行 |
| _      | 匹配单个任意字符，该字符不能为空                             |
|        |                                                              |
|        |                                                              |

```mysql
# 搜索以fish开头的产品
SELECT prod_id, prod_name FROM Products where prod_name like 'fish%';
# 搜索以fish结尾的产品
SELECT prod_id, prod_name FROM Products where prod_name like '%fish';
# 搜索以产品名中包含fish的产品
SELECT prod_id, prod_name FROM Products where prod_name like '%fish%';
# 匹配类似(两个任意字符，但是均不能为空) inch teddy bear的产品
SELECT prod_id, prod_name FROM Products where prod_name like '__ inch teddy bear'
```

### AS

alias，别名

```mysql
# cust_id 别名为 cid
SELECT cust_id as cid FROM Customers
# 价格 * 数量 起名为sum_
SELECT item_price * quantity as sum_ FROM OrderItems
```

### 函数

```mysql
# 字符串拼接
SELECT CONCAT('(', cust_address, ',', cust_city, ',', cust_country, ')') AS detail_address FROM Customers;
# 大写
SELECT  UPPER(cust_name) FROM Customers;
# 字符串替换
SELECT  REPLACE(cust_name, 'a', '-') FROM Customers;
# 求长度
SELECT  LENGTH(cust_name) FROM Customers;
# ...
```

### 汇总数据，sum，avg，count...

| SUM(column)                | 对某一列求和                         |
| -------------------------- | ------------------------------------ |
| COUNT(ALL/DISTINCT column) | 返回某列的行数，忽略NU               |
| COUNT(*) / COUNT(1)        | 对表中的行数计数，不管行中是否有空值 |
| AVG(ALL/DISTINCT column)   | 对某一列求平均值                     |
| MAX(column)                | 对某一列求最大值                     |
| MIN(column)                | 对某一列求最小值                     |

> ALL  取所有值，默认为ALL
>
> DISTINCE 只取不同的值
>

```mysql
# 平均价格
SELECT  AVG(prod_price) FROM Products;
# 价格的和
SELECT  SUM(prod_price) FROM Products;
# 不同价格的和
SELECT  SUM(DISTINCT prod_price) FROM Products;
# 价格的最大值
SELECT  MAX(prod_price) FROM Products;
# 行数
SELECT  COUNT(prod_price) FROM Products;
```

### GROUP BY 和 HAVING

notes：

+ GROUP BY 可以包含任意数目的列
+ GROUP BY子句中列出的每一列必须是检索列或者有效的表达式，如果在select中使用了表达式，则必须在GROUP BY中使用相同的表达式，不能使用别名
+ GROUP BY不允许带有长度可变的类型，如text
+ GROUP BY 会将NULL 作为一个分组返回
+ GROUP BY 必须出现在WHERE 语句之后，ORDER BY 之前

> HAVING和WHERE区别：
>
> + WHERE过滤行，HAVING过滤分组
> + WHERE在数据分组前过滤，HAVING是在分组后过滤

```mysql
# 根据vend_id 分组, 统计每组个数
SELECT vend_id, count(*) as prod_num FROM Products GROUP BY vend_id;
# 根据vend_id 分组, 统计每组个数, 筛选出每组个数大于2的
SELECT vend_id, count(*) as prod_num FROM Products GROUP BY vend_id HAVING COUNT(*) > 2;
```

### select 子句及其顺序

| 子句     | 是否必须使用         |
| -------- | -------------------- |
| SELECT   | 是                   |
| FROM     | 仅在选择表数据时使用 |
| WHERE    | 否                   |
| GROUP BY | 仅在按组聚集时使用   |
| HAVING   | 否                   |
| ORDER BY | 否                   |

```mysql
# 计算值
SELECT 1 + 2;
```



## 子查询

```mysql
# 子查询过滤, 订购了RGAN01的所有顾客id
SELECT cust_id FROM Orders WHERE order_num in (SELECT order_num FROM OrderItems WHERE prod_id = 'RGAN01')

# 子查询作为计算字段, 显示每个顾客的总订单数
# Orders.cust_id=Customers.cust_id限定了使用哪个表的cust_id
# 每个顾客都用计算子查询, 即有几个顾客就要执行几次子查询
SELECT cust_id, cust_name, (SELECT COUNT(*) FROM Orders WHERE Orders.cust_id=Customers.cust_id) as total_order_num, 10 as const from Customers
```

## 联结

联结是一种机制，用来在一条select语句中关联表。创建联结时要指定使用的表以及联结的方式。

**有时，联结可以替代子查询，联结的性能一般比子查询好。**

联结不限制表的个数，只要定义好联结条件即可

### INNER JOIN，内联结

返回两个表中都存在的数据

```mysql
# 查询每个产品的生产商名字, WHERE作为联结条件, 没有WHERE语句, 两个表会做笛卡尔积
SELECT v.vend_name, p.prod_name, p.prod_price FROM Vendors as v, Products as p WHERE v.vend_id = p.vend_id;
# 没指定联结条件, 两个表会做笛卡尔积, 不管逻辑上是否能配对
SELECT v.vend_name, p.prod_name, p.prod_price FROM Vendors as v, Products as p;

# 联结的另一种写法
SELECT v.vend_name, p.prod_name, p.prod_price FROM Vendors as v INNER JOIN Products as p ON v.vend_id = p.vend_id;

# 订购了RGAN01的所有顾客id, 使用联结实现子查询中实现的语句
SELECT cust_id from Orders, OrderItems where Orders.order_num = OrderItems.order_num AND OrderItems.prod_id = 'RGAN01';

# 订购了RGAN01的所有顾客id和顾客姓名
SELECT Customers.cust_id, Customers.cust_name from Customers, Orders, OrderItems where Orders.order_num = OrderItems.order_num AND OrderItems.prod_id = 'RGAN01' AND Customers.cust_id=Orders.cust_id;
```

### 自联结

一条查询语句中，同一个表使用了不止一次，自己联结自己的数据，所以叫自联结

```mysql
# 查找与Jim Jones同一个家公司的顾客
SELECT c1.cust_name, c1.cust_id, c1.cust_contact FROM Customers as c1, Customers as c2 WHERE c1.cust_name = c2.cust_name AND c2.cust_contact='Jim Jones';
```

### LEFT/RIGHT JOIN，外联结

```
LEFT OUTER JOIN = LEFT JOIN    以左表 join 右表, 左表中的所有行都在
RIGHT OUTER JOIN = RIGHT JOIN  以右表 join 左表, 右表中的所有行都在
```

> mysql不支持全联结

```mysql
# 查看下了订单的顾客信息
SELECT C.cust_id, C.cust_name, O.order_num from Customers AS C, Orders AS O WHERE O.cust_id = C.cust_id;
# OR
SELECT C.cust_id, C.cust_name, O.order_num from Customers AS C INNER JOIN Orders AS O ON O.cust_id = C.cust_id;

# 查看所有顾客的下单信息, 包含未下单的
SELECT C.cust_id, C.cust_name, O.order_num from Customers AS C LEFT JOIN Orders AS O ON O.cust_id = C.cust_id
```

## UNION

组合，注意

+ UNION必须由两条或以上的select语句组成，语句之间用UNION分隔
+ UNION的查询中必须包含相同的列，次序可以不同
+ 数据类型必须兼容
+ 对UNION排序时，ORDER BY只能出现一次，并且是语句最后

```mysql
# 重复的行会被自动去掉
SELECT cust_id FROM Customers WHERE cust_id >= 1000000002
UNION
SELECT cust_id FROM Customers WHERE cust_id >= 1000000003
ORDER BY cust_id

# 不想去掉重复行可用ALL
SELECT cust_id FROM Customers WHERE cust_id >= 1000000002
UNION ALL
SELECT cust_id FROM Customers WHERE cust_id >= 1000000003
ORDER BY cust_id

```

## INSERT

```mysql
# 各列需以添加的顺序出现
# 如果表结构出现变化, 这种插入语句是不兼容的
INSERT INTO Orders VALUES ('200010', '2012-02-08 00:00:00', '1000000001');

# 推荐使用这种, 表后面明确给出了列名. 表结构改变后, 该语句依旧能使用
INSERT INTO Orders (order_num, order_date, cust_id) VALUES ('200011', '2012-02-08 00:00:00', '1000000001');

# 插入检索的数据, 在创建一个和Orders一样的表Orders_copy
CREATE TABLE Orders_copy LIKE Orders;   
INSERT INTO Orders_copy (order_num, order_date, cust_id) SELECT order_num, order_date, cust_id from Orders
```



## UPDATE

```mysql
# 如果不加WHERE限制条件, 将改变所有列
UPDATE Customers SET cust_email='test', cust_city='CHINA' WHERE cust_id='1000000001';
```

## DELETE

```mysql
# 如果省略了WHERE将删除所有数据
DELETE FROM  Customers WHERE cust_id='1000000001';
```



## 视图（VIEW）

虚拟的表，不包含数据，只是一个查询语句。它们包含的不是数据而是根据需要检索数据的查询。视图可以视为对SELECT语句的封装，可以用来简化数据处理，重新格式化/保护基础数据

```mysql
# 删除视图
DROP VIEW OrderDetail;

# 创建视图
CREATE VIEW OrderDetail AS 
SELECT
	C.cust_id AS cust_id,
	C.cust_name AS cust_name,
	O.order_num AS order_num,
	OI.order_item AS order_item,
	OI.prod_id AS prod_id
FROM
	(
		Customers AS C,
		Orders AS O,
		OrderItems AS OI
	)
WHERE
	(
		(C.cust_id = O.cust_id)
		AND (O.order_num = OI.order_num)
	)
ORDER BY
	C.cust_id
```

> + 可以将视图当做正常的表使用，适用于表的查询语句基本都适用于视图
>
> + 视图不能和表重名
>
> + 视图可以简化查询过程
> + 使用视图时，传递给视图的WHERE语句会与视图中的WHERE语句自动组合

```mysql
# 从虚拟表中查询
SELECT * FROM OrderDetail WHERE prod_id='BR03'; 
```

# Notes

+ 数据库软件是数据库管理系统（DBMS），如MYSQL。

+ sql，structured query language（结构化查询语言）

+ 对表做比较大的改动时，一定要备份表，不然天知道会出现什么问题。

+ 不同数据库中，表名可以相同；相同数据库中表明要唯一

+ 主键：一列/一组列，其值能够唯一标识表中每一行，不能为NULL

+ 关键字不能用作表/列的名字

+ 多条sql语句必须以分号分隔

+ sql语句不区分大小写，但是推荐奖关键字大写

+ 子句：sql语句由子句组成，有些子句是必须的，有些这是可选的，一个子句通常由一个关键字加上所提供的数据组成

+ NULL  是一个特殊的值，与字段0、空字符串不同

+ [唯一索引不能设置为NULL，不然可以插入重复值](https://yemengying.com/2017/05/18/mysql-unique-key-null/)

  > MySQL 官方文档上已经明确说了这一点， 唯一性索引是允许多个 NULL 值的存在的
  >
  > A UNIQUE index creates a constraint such that all values in the index must be distinct. An error occurs if you try to add a new row with a key value that matches an existing row. For all engines, a UNIQUE index allows multiple NULL values for columns that can contain NULL.

+ 更新和删除数据时，一定要注意筛选条件，不然可能更新或删除所有数据

+ 主键和唯一索引的区别

  1. 一张表中可以有多个唯一索引，但是只可以有一个主键
  2. 唯一索引可以为NULL，但是不推荐这么做。
  3. 唯一索引不能用来定义外键


[1]: http://forta.com/books/0672336073/

