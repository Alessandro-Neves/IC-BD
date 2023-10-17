-- Return tuples violations as (id1, id2)[]
-- [JOIN, SELF JOIN, DISTINCT, GROUP BY]

-- [JOIN]
SELECT t1.id, t2.id
FROM T t1 
JOIN T t2  ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate;

-- [GROUP BY]
SELECT t1.id, t2.id
FROM T t1, T t2
  GROUP BY t1.id, t2.id, t1.State, t2.State, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.State = t2.State AND t1.Rate < t2.Rate AND t1.Salary > t2.Salary;







--(REMOVIDO) Só faz sentido quando pode acontecer de duas tuplas terem o mesmo identificador, mas nesse caso isto
-- tem que ser tratado em todos as outras consultas, então é um problema separado
-- [DISTINCT]
SELECT DISTINCT t1.id, t2.id
FROM T t1, T t2 
WHERE t1.State = t2.State  AND t1.Salary > t2.Salary  AND t1.Rate < t2.Rate;