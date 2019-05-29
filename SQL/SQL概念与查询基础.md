##                                         第一章  SQL基础



#### DDL**（数据定义语言）：用来创建或者删除存储数据用的数据库以及数据库中的表等对象**Data  Definition  Language

- `CREATE：创建数据库和表等对象` 
- `DROP： 删除数据库和表等对象` 
- `ALTER： 修改数据库和表等对象的结构`

#### DML（数据操纵语言）用来查询或者变更 表中的记录。Data  Manipulation  Language

- `SELECT：查询表中的数据` 
- `INSERT：向表中插入新数据` 
- `UPDATE：更新表中的数据` 
- `DELETE：删除表中的数据`

#### DCL（数据控制语言）用来确认或者取消对数据 库中的数据进行的变更。除此之外，还可以对 RDBMS的用户是否有权限 操作数据库中的对象（数据库表等）进行设定。Data  Control  Language

- `COMMIT： 确认对数据库中的数据进行的变更` 
- `ROLLBACK： 取消对数据库中的数据进行的变更` 
- `GRANT： 赋予用户操作权限`
- `REVOKE： 取消用户的操作权限`



------

##                                                数据类型：

- **INTEGER**   ：整型
- **DATE**   :日期型
- **CHAR**  ： 定长字符串
- **VARCHAR**  ：可变长字符串

####                             `约束：主键约束(PRIMARY KEY )  ,非空约束(NOT NULL)`



------



##                                       表的创建、删除、更新

- #### **数据表Product**

![1552117029864](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552117029864.png)

- #### 创建数据库shop

```mysql
CREATE DATABASE shop;
```



- #### 创建Product表

```mysql
CREATE TABLE Product (
    product_id CHAR(4) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_type VARCHAR(32) NOT NULL,
    sale_price INTEGER,
    purchase_price INTEGER,
    regist_date DATE,
    PRIMARY KEY (product_id)
);
```



- #### 删除Product表 

```mysql
DROP TABLE Product;
```



- #### 添加一列可以存储100位的可变长字符串的product_name_pinyin列

```mysql
ALTER TABLE Product ADD COLUMN product_name_pinyin VARCHAR(100);
```



- #### 删除product_name_pinyin列

```mysql
ALTER TABLE Product DROP COLUMN product_name_pinyin;
```



- #### 更改表名

```mysql
RENAME TABLE Poduct to Product; 
```



- #### 更改列名

```mysql
alter table product change column reg_date regist_date date;
```



- #### 向Product表中插入数据

```mysql
START TRANSACTION;

INSERT INTO Product VALUES ('0001', 'T恤衫', '衣服', 1000, 500, '2009-09-20'); 
INSERT INTO Product VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11'); 
INSERT INTO Product VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL); 
INSERT INTO Product VALUES ('0004', '菜刀', '厨房用具',   3000, 2800, '2009-09-20'); 
INSERT INTO Product VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15'); 
INSERT INTO Product VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20'); 
INSERT INTO Product VALUES ('0007', '擦菜板', '厨房用具', 880, 790, '2008-04-28'); 
INSERT INTO Product VALUES ('0008', '圆珠笔', '办公用品', 100, NULL,'2009-11-11');
 
COMMIT;
```



------





##                                         第二章：基础查询

###                                            1   ：  SELECT语句基础

- #### 从Product表中输出3列 

```mysql
SELECT 
    product_id, product_name, purchase_price
FROM
    Product;
```

![1552118106805](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552118106805.png)



- #### 为列设定别名 

```mysql
SELECT 
    product_id AS '商品编号',   -- 中文别名用""
    product_name AS '商品名称',
    purchase_price AS '进货单价'
FROM
    Product;

```

![1552118877827](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552118877827.png)



- #### 使用DISTINCT删除product_type列中重复的数据 

```mysql
SELECT DISTINCT     -- 　对含有NULL数据的列使用DISTINCT关键字时,所有NULL的数据会被合并为一条
    product_type    --   DISTINCT 关键字只能用在第一个列名之前
FROM
    Product;
```

![1552118980423](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552118980423.png)



- #### 根据WHERE语句来选择记录

```mysql
-- 用来选取product_type列为'衣服'的记录的SELECT语句 
SELECT 
    product_name, product_type
FROM
    Product
WHERE
    product_type = '衣服';
    
-- 首先通过 WHERE 子句查询出符合指定条件的记录，然后再选取出SELECT 语句指定的列
```

![1552119411617](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552119411617.png)



###                                     2  ： 算术、比较、逻辑运算符                  

- ### 算术运算符  +  -  *  /

```mysql
SELECT 
    product_name, sale_price, sale_price * 2 AS 'sale_price_x2'
FROM
    Product;
-- 所有包含 NULL 的计算，结果肯定是 NULL
```

![1552119747759](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552119747759.png)





- ### 比较运算符   =   <>   >   <   >=   <=   

```mysql
SELECT 
    product_name, product_type
FROM
    Product
WHERE
    sale_price = 500;
/* 字符串类型的数据原则上按照字典顺序进行排序
   不能对NULL使用比较运算符
   希望选取NULL记录时，需要在条件表达式中使用IS NULL运算符。
   希望选取不是NULL的记录时，需要在条件表达式中使用IS NOT NULL运算符。
*/
```

![1552119848874](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552119848874.png)





- ### 逻辑运算符： AND ,OR ,NOT

```mysql
SELECT 
    product_name, product_type, regist_date
FROM
    Product
WHERE
    product_type = '办公用品'                           
        AND (regist_date = '2009-09-11'     -- AND 运算符优先于 OR 运算符
        OR regist_date = '2009-09-20');

```

![1552120210379](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552120210379.png)