
-- [JOIN + GROUP_CONCAT]
SELECT t1.id, GROUP_CONCAT(t2.id) as T2_ID_List
FROM T t1
JOIN T t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
GROUP BY t1.id;

-- [JOIN + SUBQUERY + GROUP_CONCAT]
SELECT t1.id, (
    SELECT GROUP_CONCAT(t2.id)
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) as T2_ID_List
FROM T t1 WHERE LENGTH(T2_ID_List) > 0;

-- [JOIN + SUBQUERY + STRING_AGG]
SELECT t1.id, (
    SELECT STRING_AGG(t2.id, ', ')
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) as T2_ID_List
FROM T t1 WHERE LENGTH(T2_ID_List) > 0;

-- [JOIN + SUBQUERY + ARRAY_TO_STRING]
SELECT t1.id, (
    SELECT ARRAY_TO_STRING(ARRAY_AGG(t2.id), ', ')
    FROM T t2
    WHERE t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
) as T2_ID_List
FROM T t1 WHERE LENGTH(T2_ID_List) > 0;

-- [DISTINC + GROUP_CONCAT]
SELECT t1.id, GROUP_CONCAT(t2.id) as T2_ID_List
FROM T t1
JOIN T t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate
GROUP BY t1.id;



