-- t1.salario > t2.bonus

SELECT *
FROM funcionarios t1
JOIN departamentos t2 ON t1.departamento_id = t2.id
WHERE t1.salario > t2.bonus;