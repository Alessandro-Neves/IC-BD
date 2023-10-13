-- Return tuples violations as (id1, id2)[]
-- [JOIN, SELF JOIN, DISTINCT, GROUP BY]

-- [JOIN] (OK)
SELECT t1.id, t2.id
FROM T t1 
[SELF] JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

-- Notation
SELECT t1.id, t2.id
FROM T t1
JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>];


-- [DISTINCT] (OK)
SELECT DISTINCT t1.id, t2.id
FROM T t1, T t2 
WHERE t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

SELECT DISTINCT t1.id, t2.id
FROM T t1, T t2
WHERE [where_conditions as <t1.column operator t2.column>];


-- [GROUP BY] (OK)
SELECT t1.id, t2.id
FROM T t1, T t2 
  WHERE t1.State = t2.State 
  GROUP BY t1.id, t2.id, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.Rate < t2.Rate AND t1.Salary > t2.Salary;

-- OR

SELECT t1.id, t2.id
FROM T t1, T t2
  GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary;