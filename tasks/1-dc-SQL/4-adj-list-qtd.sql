
-- [JOIN + GROUP BY]
SELECT t1.id, COUNT(*)
FROM T t1 JOIN T t2 
ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
GROUP BY t1.id;

-- [DISTINCT + GROUP BY]
SELECT t1.id, COUNT(*)
FROM T t1 JOIN T t2 
ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
GROUP BY t1.id;

-- [SUBQUERY]
SELECT t1.id, (
    SELECT COUNT(*)
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) as CountResult
FROM T t1 WHERE CountResult > 0;

-- [EXISTS]
SELECT t1.id, COUNT(*)
FROM T t1
WHERE EXISTS (
    SELECT 1
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
)
GROUP BY t1.id;



















-- Queries como essa são desconsideradas já que fazem trabalho desnecessário (SUBQUERY faz o mesmo com alias)
SELECT t1.id, (
    SELECT COUNT(*)
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) FROM T t1
WHERE (
    SELECT COUNT(*)
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) > 0;