-- Return set of tuples ids on some violation
-- [UNION + JOIN]

SELECT t1.ID FROM T t1 
JOIN T t2 
  ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
UNION
  SELECT t2.ID FROM T t1 
  JOIN T t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate;

-- [UNION + EXISTS + JOIN]

SELECT t1.ID FROM T t1 
WHERE EXISTS (
  SELECT 1 FROM T t2
  WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
)
UNION
  SELECT t2.ID FROM T t1 
  JOIN T t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate;

-- [UNION + GROUP BY]
SELECT t1.ID FROM T t1, T t2 
  GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary
UNION
  SELECT t2.ID FROM T t1, T t2
  GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary;


-- [UNION + EXISTS + GROUP BY]
SELECT t1.ID FROM T t1 
WHERE EXISTS (
  SELECT 1 FROM T t2
  WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
)
UNION
  SELECT t2.ID FROM T t1, T t2
  GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary;


















-- (REMOVIDO)
-- [CONCAT + SUBQUERY]
SELECT CONCAT(
  SELECT CONCAT(t1.id, ',', t2.id)
  FROM T t1 
  JOIN T t2  ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
);

