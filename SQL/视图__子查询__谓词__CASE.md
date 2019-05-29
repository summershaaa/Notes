##                                     第五章  ： 视图与子查询



- #### 创建视图

```mysql
CREATE VIEW 视图名称(<视图列名1>, <视图列名2>, ……) 
AS 
<SELECT语句>

CREATE VIEW ProductSum (product_type , cnt_product) 
AS
    SELECT 
        product_type, COUNT(*)
    FROM
        Product
    GROUP BY product_type;
   
-- 表中存储的是实际数据，而视图中保存的是从表中取出数据所使用的SELECT语句
-- 应该将经常使用的SELECT语句做成视图
-- 定义视图时不能使用ORDER BY子句
-- 通过汇总得到的视图无法进行更新
```

![1552267970073](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552267970073.png)



- #### 删除视图 

```mysql
DROP VIEW ProductSum; 
```



- ###  子查询

```mysql
-- 在FROM子句中直接书写定义视图的SELECT语句
-- 子查询就是将用来定义视图的SELECT语句直接用于FROM子句当中
-- 子查询作为内层查询会首先执行。

SELECT 
    product_type, cnt_product
FROM
    (SELECT 
        product_type, COUNT(*) AS cnt_product
    FROM
        Product
    GROUP BY product_type) AS ProductSum;

```

![1552268791017](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552268791017.png)



- #### 标量子查询 

```mysql
-- 标量子查询就是返回单一值的子查询。
-- 选取出销售单价（sale_price）高于全部商品的平均单价的商品
SELECT 
    product_id, product_name, sale_price
FROM
    Product
WHERE
    sale_price > (SELECT 
            AVG(sale_price)
        FROM
            Product);
```

![1552268921365](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552268921365.png)



- #### 在SELECT子句中使用标量子查询 

```mysql
SELECT 
    product_id,
    product_name,
    sale_price,
    (SELECT 
            AVG(sale_price)
        FROM
            Product) AS avg_price
FROM
    Product;
/*
能够使用常数或者列名的地方，无论是 SELECT 子句、GROUP BY 子句、HAVING 子句，还是 ORDER BY 子句，几乎所有的地方都可以使用标量子查询 
*/
```

![1552269020542](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552269020542.png)



- ### 关联子查询

```mysql
-- 通过关联子查询按照商品种类对平均销售单价进行比较
-- 在细分的组内进行比较时，需要使用关联子查询
SELECT 
    product_type, product_name, sale_price
FROM
    Product AS P1
WHERE
    sale_price > (SELECT 
            AVG(sale_price)
        FROM
            Product AS P2
        WHERE
            P1.product_type = P2.product_type
        GROUP BY product_type);

```

![1552269968718](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552269968718.png)



##                                                   谓词

- #### LIKE谓词——字符串的部分一致查询 

#####                                                                                SampleLike表

![1552270199916](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270199916.png)

- #### 使用LIKE进行前方一致查询 

```mysql
SELECT 
    *
FROM
    SampleLike
WHERE
    strcol LIKE 'ddd%';
```

![1552270263033](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270263033.png)



- #### 　使用LIKE进行中间一致查询 

```mysql
SELECT 
    *
FROM
    SampleLike
WHERE
    strcol LIKE '%ddd%';
```

![1552270316667](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270316667.png)



- #### 使用LIKE进行后方一致查询 

```mysql
SELECT 
    *
FROM
    SampleLike
WHERE
    strcol LIKE '%ddd';
```

![1552270364374](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270364374.png)



- #### 使用LIKE和_（下划线）进行后方一致查询 

```mysql
SELECT 
    *
FROM
    SampleLike
WHERE
    strcol LIKE 'abc_ _';

```

![1552270450090](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270450090.png)



### BETWEEN谓词——范围查询 

- #### 选取销售单价为100～1000日元的商品

```mysql
SELECT 
    product_name, sale_price
FROM
    Product
WHERE
    sale_price BETWEEN 100 AND 1000;

```

![1552270545168](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270545168.png)



###                         IS NULL、IS NOT NULL——判断是否为NULL 

- #### 选取进货单价（purchase_price）不为NULL的商品

```mysql
SELECT 
    product_name, purchase_price
FROM
    Product
WHERE
    purchase_price IS NOT NULL;
```

![1552270635847](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270635847.png)



### IN谓词——OR的简便用法 

- #### 通过IN来指定多个进货单价进行查询 

```mysql
SELECT 
    product_name, purchase_price
FROM
    Product
WHERE
    purchase_price IN (320 , 500, 5000);
-- 在使用 IN 和NOT IN 时是无法选取出 NULL 数据的
```

![1552270723988](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270723988.png)

- #### 使用NOT IN进行查询时指定多个排除的进货单价进行查询 

```mysql
SELECT 
    product_name, purchase_price
FROM
    Product
WHERE
    purchase_price NOT IN (320 , 500, 5000);
```

![1552270807402](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270807402.png)





- ### 使用子查询作为IN谓词的参数

#####                                                                               ProductShop表

![1552270890642](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552270890642.png)



- #### 使用子查询作为IN的参数 

```mysql
-- 取得“在大阪店销售的商品的销售单价” 
SELECT 
    product_name, sale_price
FROM
    Product
WHERE
    product_id IN (SELECT 
            product_id
        FROM
            ShopProduct
        WHERE
            shop_id = '000C');

```

![1552271538705](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552271538705.png)



##                                              CASE表达式

- #### 搜索CASE表达式

```mysql
CASE   WHEN <求值表达式> THEN <表达式>     
       WHEN <求值表达式> THEN <表达式>     
       WHEN <求值表达式> THEN <表达式>            
       ELSE <表达式> 
END

-- 通过CASE表达式将A～C的字符串加入到商品种类当中 
SELECT 
    product_name,
    CASE
        WHEN product_type = '衣服' THEN 'A ：' || product_type
        WHEN product_type = '办公用品' THEN 'B：' || product_type
        WHEN product_type = '厨房用具' THEN 'C ：' || product_type
        ELSE NULL
    END AS abc_product_type
FROM
    Product;

```

![1552271728351](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552271728351.png)



- #### 使用CASE表达式进行行列转换 

```mysql
-- 对按照商品种类计算出的销售单价合计值进行行列转换 
SELECT 
    SUM(CASE
        WHEN product_type = '衣服' THEN sale_price
        ELSE 0
    END) AS sum_price_clothes,
    SUM(CASE
        WHEN product_type = '厨房用具' THEN sale_price
        ELSE 0
    END) AS sum_price_kitchen,
    SUM(CASE
        WHEN product_type = '办公用品' THEN sale_price
        ELSE 0
    END) AS sum_price_office
FROM
    Product;

```

![1552271975928](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1552271975928.png)



- #### 简单CASE表达式 

```mysql
CASE <表达式>    WHEN <表达式> THEN <表达式>   
                WHEN <表达式> THEN <表达式>    
                WHEN <表达式> THEN <表达式>     
                ELSE <表达式> 
END

SELECT 
    product_name,
    CASE product_type
        WHEN '衣服' THEN 'A ：' || product_type
        WHEN '办公用品' THEN 'B：' || product_type
        WHEN '厨房用具' THEN 'C ：' || product_type
        ELSE NULL
    END AS abc_product_type
FROM
    Product;

```

​	