--- ** Return nº violations **
-- [JOIN]
SELECT COUNT(*)
FROM T t1 
[CROSS] JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>];

-- [DISTINCT]
SELECT DISTINCT COUNT(*)
FROM T t1, T t2
WHERE [where_conditions as <t1.column operator t2.column>];

-- [GROUP BY]
SELECT COUNT(*)
FROM (
  SELECT t1.id, t2.id
    FROM T t1, T t2
    GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary
    HAVING t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary
);