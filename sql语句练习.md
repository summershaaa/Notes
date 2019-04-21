

**1. 查询” 01 “课程比” 02 “课程成绩高的学生的信息及课程分数**

```mysql
SELECT 
    s.*, a.s_score score_01, b.s_score score_02
FROM
    Student s,
    (SELECT s_id, s_score FROM Score WHERE c_id = '01') a,
    (SELECT s_id, s_score FROM Score WHERE c_id = '02') b
WHERE
    s.s_id = a.s_id AND a.s_id = b.s_id AND a.s_score > b.s_score;
```

![1553513675733](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553513675733.png)

**2. 查询平均成绩大于等于 60 分的同学的学生编号和学生姓名和平均成绩**

```mysql
SELECT 
    s.s_id, s.s_name, ROUND(AVG(c.s_score), 2) avg_score
FROM
    Student s,
    Score c
WHERE
    s.s_id = c.s_id
GROUP BY s.s_id
HAVING avg_score >= 60;
```

![1553513691804](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553513691804.png)



**3. 查询在 Score表存在成绩的学生信息**

```mysql
 SELECT 
    *
FROM
    Student
WHERE
    s_id IN (SELECT s_id FROM Score 
               WHERE s_score IS NOT NULL);
```

![1553514414927](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553514414927.png)



**4. 查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩(没成绩的显示为 null )**

```mysql
SELECT 
    s.s_id,
    s.s_name,
    COUNT(c.c_id) cnt_course,
    SUM(c.s_score) sum_score
FROM
    Student s
        LEFT JOIN
    Score c ON s.s_id = c.s_id
GROUP BY s.s_id;
```

![1553514387671](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553514387671.png)



**4.1 查有成绩的学生信息**

```mysql
 SELECT 
    s.*,
    COUNT(c.c_id) cnt_course,
    SUM(CASE WHEN c.c_id = '01' THEN c.s_score ELSE 0 END) score_01,
    SUM(CASE WHEN c.c_id = '02' THEN c.s_score ELSE 0 END) score_02,
    SUM(CASE WHEN c.c_id = '03' THEN c.s_score ELSE 0 END) score_03,
    SUM(c.s_score) sum_score
FROM
    Student s,
    Score c
WHERE
    s.s_id = c.s_id
GROUP BY s.s_id;
```

![1553514842813](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553514842813.png)



**5. 查询「李」姓老师的数量**

```mysql
SELECT 
    COUNT(*)
FROM
    Teacher
WHERE
    t_name LIKE '李%';
```

![1553516360631](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553516360631.png)



**6. 查询学过「张三」老师授课的同学的信息**

```mysql
SELECT 
    s.*
FROM
    Student s
WHERE
    s.s_id IN (SELECT sc.s_id FROM Score sc
                   WHERE sc.c_id = 
                   (SELECT c_id 
                       FROM Course c INNER JOIN Teacher t 
                       ON c.t_id = t.t_id AND t.t_name = '张三'));
```

![1553516332705](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553516332705.png)



**7. 查询没有学全所有课程的同学的信息**

```mysql
SELECT 
    s.*
FROM
    Student s
WHERE
    s.s_id IN (SELECT sc.s_id FROM Score sc
			   GROUP BY sc.s_id
               HAVING COUNT(sc.c_id) < (SELECT COUNT(*) 
                                              FROM Course)
                                              );
```

![1553517098137](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553517098137.png)



**8. 查询至少有一门课与学号为” 01 “的同学所学相同的同学的信息**

```mysql
SELECT 
    *
FROM
    Student
WHERE
    s_id IN (SELECT DISTINCT s_id FROM Score
			 WHERE c_id IN (SELECT  c_id FROM Score
                            WHERE s_id = '01')
                            );
```

![1553519079648](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553519079648.png)



**10. 查询没学过”张三”老师讲授的任一门课程的学生姓名**

```mysql
 SELECT 
    s.s_name name
FROM
    Student s
WHERE
    s.s_name NOT IN (SELECT 
            s.s_name
        FROM
            Student s,
            Course c,
            Score sc,
            Teacher t
        WHERE
            sc.s_id = s.s_id AND 
            t.t_id = c.t_id  AND 
            t.t_name = '张三'AND 
			sc.c_id = c.c_id);
```

![1553519122173](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553519122173.png)



**11. 查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩**

```mysql
SELECT 
    s.s_id, s.s_name, ROUND(AVG(sc.s_score),2) avg_score
FROM
    Student s,
    Score sc
WHERE
    s.s_id = sc.s_id AND sc.s_score < 60
GROUP BY s.s_id
HAVING COUNT(*) >= 2;
```

![1553574757383](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553574757383.png)



**12. 检索” 01 “课程分数小于 60，按分数降序排列的学生信息**

```mysql
 SELECT 
    s.*, sc.s_score score_01
FROM
    Student s,
    Score sc
WHERE
    sc.c_id = '01' AND sc.s_score < 60
        AND s.s_id = sc.s_id
ORDER BY sc.s_score DESC;
```

![1553576095024](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553576095024.png)



**13. 按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩**

```mysql
 SELECT 
    s_id,
    SUM(CASE WHEN c_id = '01' THEN s_score ELSE 0 END) score_01,
    SUM(CASE WHEN c_id = '02' THEN s_score ELSE 0 END) score_02,
    SUM(CASE WHEN c_id = '03' THEN s_score ELSE 0 END) score_03,
    AVG(s_score) avg_score
FROM
    Score
GROUP BY s_id
ORDER BY avg_score DESC;
```

![1553576075137](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553576075137.png)



14. 查询各科成绩最高分、最低分和平均分，以如下形式显示：课程 ID，课程 name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率(及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90）。 
    要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
```mysql
 SELECT 
    c.c_id AS 课程号,
    c.c_name AS 课程名称,
    COUNT(*) AS 选课人数,
    MAX(sc.s_score) AS 最高分,
    MIN(sc.s_score) AS 最低分,
    AVG(sc.s_score) AS 平均分,
    SUM(CASE WHEN sc.s_score >= 60 THEN 1 ELSE 0 END) / COUNT(*) AS 及格率,
    SUM(CASE WHEN sc.s_score >= 70 AND sc.s_score < 80 THEN 1 ELSE 0 END) / COUNT(*) AS 中等率,
    SUM(CASE WHEN sc.s_score >= 80 AND sc.s_score < 90 THEN 1 ELSE 0 END) / COUNT(*) AS 优良率,
    SUM(CASE WHEN sc.s_score >= 90 THEN 1 ELSE 0 END) / COUNT(*) AS 优秀率
FROM
    Score sc,
    Course c
WHERE
    c.c_id = sc.c_id
GROUP BY c.c_id
ORDER BY COUNT(*) DESC , c.c_id ASC;
```

![1553863678297](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553863678297.png)



**17. 统计各科成绩各分数段人数：课程编号，课程名称，[100-85]，[85-70]，[70-60]，[60-0] 所占百分比**

```mysql
SELECT 
    c.c_id 课程号,
    c.c_name 课程名,
    SUM(CASE WHEN sc.s_score < 60 THEN 1 ELSE 0 END) / COUNT(*) 0_60,
    SUM(CASE WHEN sc.s_score >= 60 AND sc.s_score < 70 THEN 1 ELSE 0 END) / COUNT(*) 60_70,
    SUM(CASE WHEN sc.s_score >= 70 AND sc.s_score < 85 THEN 1 ELSE 0 END) / COUNT(*) 70_85,
    SUM(CASE WHEN sc.s_score >= 85 AND sc.s_score <= 100 THEN 1 ELSE 0 END) / COUNT(*) 85_100
FROM
    Course c,
    Score sc
WHERE
    c.c_id = sc.c_id
GROUP BY c.c_id;
```

![1553864566617](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553864566617.png)



**20. 查询出只选修两门课程的学生学号和姓名**

```mysql
 SELECT 
    s.s_id, s.s_name
FROM
    Student s
WHERE
    s.s_id IN (SELECT s_id 
                FROM Score
                GROUP BY s_id
			    HAVING COUNT(*) = 2);
```

![1553864910589](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553864910589.png)



**22. 查询名字中含有「风」字的学生信息**

```sql
SELECT 
    s.*
FROM
    Student s
WHERE
    s.s_name LIKE '%风%';
```

![1553865024239](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553865024239.png)



**24. 查询 1990 年出生的学生名单**

```mysql
SELECT 
    *
FROM
    Student
WHERE
    EXTRACT(YEAR FROM s_birth) = 1990;
```

![1553865122365](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553865122365.png)



**40. 查询各学生的年龄，只按年份来算**

```mysql
SELECT 
    s_name name, YEAR(NOW()) - YEAR(s_birth) age
FROM
    Student;
```

![1553865412354](C:\Users\WinJX\AppData\Roaming\Typora\typora-user-images\1553865412354.png)



