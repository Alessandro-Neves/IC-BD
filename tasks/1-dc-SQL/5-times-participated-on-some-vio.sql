-- 
SELECT ID, COUNT(*)
FROM (
  SELECT t1.ID
    FROM T t1
    JOIN T t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
  UNION ALL
  SELECT t2.ID
    FROM T t1 JOIN T t2 
    ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
)
GROUP BY ID;