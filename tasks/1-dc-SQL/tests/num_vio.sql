SELECT COUNT(*)
FROM T t1
JOIN T t2
  ON [...conditions]
  AND t1.id <> t2.id;

SELECT COUNT(*)
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

-- 428
SELECT t1.ID
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

-- 112
SELECT t1.ID 
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate
GROUP BY t1.ID;

-- 112
SELECT COUNT(*)
FROM T t1
WHERE EXISTS (
  SELECT 1
  FROM T t2
  WHERE t1.State = t2.State
    AND t1.Salary > t2.Salary
    AND t1.Rate < t2.Rate
  LIMIT 1
) LIMIT 1;

-- ----------------------------

CREATE TABLE T AS SELECT * FROM 'tax_100k_noisy_0.5.csv';
CREATE SEQUENCE T_SEQ START 1;
ALTER TABLE T ADD COLUMN ID INT;
UPDATE T SET ID = nextval('T_SEQ');