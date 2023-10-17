-- Consigo derivar uma query para encontrar DC da query para encontrar FD:
-- Encontrar FCs:
SELECT
    column_set_1,
    column_set_2
FROM
    your_table
GROUP BY
    column_set_1, column_set_2
HAVING
    COUNT(*) > 1;

-- Encontrar violações de FCs:
-- [GROUP BY]
SELECT
    column_set_1,
    column_set_2
FROM
    your_table
GROUP BY
    column_set_1, column_set_2
HAVING
    COUNT(DISTINCT column_set_2) > 1;


-- Para encontrar violações de FD envolve 'apenas' o agrupamento dos conjuntos de valores e posteriormente verificar se para cada agrupamento 'filho' 
-- possui cardinalidade > 1.
-- Porém não consigo (até agora) utilizar algo parecido para encontrar violações de DCs pq nesse caso eu preciso 
-- obrigatoriamente utilizar a avaliação dos predicados da DC (WHERE ou HAVING)
-----------------------------------------------------------------------------------------------------------------------


-- Consigo derivar uma query para encontrar DC da query para encontrar FD:


SELECT
    column_set_1,
    column_set_2
FROM (
    SELECT
        column_set_1,
        column_set_2,
        COUNT(DISTINCT column_set_2) OVER (PARTITION BY column_set_1) AS distinct_count
    FROM
        your_table
) AS subquery
WHERE
    distinct_count > 1;