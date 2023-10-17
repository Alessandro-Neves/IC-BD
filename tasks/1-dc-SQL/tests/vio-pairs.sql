-- Retorno: Pares de violações [(1, 3), (4, 5)]

----------------------------
SELECT t1.id, t2.id
FROM T t1
JOIN T t2
  ON [...conditions]
  AND t1.id <> t2.id;

-- Exemplo
SELECT t1.id, t2.id
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate
  AND t1.id <> t2.id;
----------------------------

SELECT t1.id, t2.id
FROM T t1
JOIN T t2
ON t1.State = t2.State
WHERE t1.Salary > t2.Salary
  AND t1.Rate < t2.Rate
  AND EXISTS (
    SELECT 1
    FROM T t3
    WHERE t3.State = t1.State
  );

SELECT *
FROM T t1
JOIN T t2
ON t1.State = t2.State
WHERE t1.Salary > t2.Salary
  AND t1.Rate < t2.Rate
  AND EXISTS (
    SELECT 1
    FROM T t3
    WHERE t3.State = t1.State
  );

SELECT t1.id
FROM T t1
WHERE EXISTS (
    SELECT 1
    FROM T t2
    WHERE t1.State = t2.State
    AND t1.Salary > t2.Salary
    AND t1.Rate < t2.Rate
  );


----------------------------
WITH CTE AS (
  SELECT id, State, Salary, Rate
  FROM T
)
SELECT *
FROM CTE t1
JOIN CTE t2
ON t1.State = t2.State
WHERE t1.Salary > t2.Salary
  AND t1.Rate < t2.Rate;


SELECT *
FROM T t1
JOIN T t2
ON t1.State = t2.State
WHERE t1.Salary > t2.Salary
  AND t1.State = t2.State
  AND EXISTS (
    SELECT 1
    FROM T t3
    WHERE t3.Rate >= t1.Rate
  );
---------------------------------

SELECT *
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate
  AND t1.id <> t2.id;


EXPLAIN SELECT t1.State, Count(*) FROM T t1 WHERE t1.State = 'DE' GROUP BY t1.State;

-- Como eu usaria GROUP BY para melhorar performance se ele só é feito depois da projeção final


