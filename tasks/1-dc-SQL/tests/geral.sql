-- no maximo um subquery aninhada

--- ** Return (id, qtd_violations_rel)[] **
-- [JOIN + COUNT(*)]
SELECT t1.id, COUNT(*)
FROM T t1 
[SELF] JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate
GROUP BY t1.id;
[ORDER BY COUNT(*)]

--- Notation
SELECT t1.id, COUNT(*)
FROM T t1
JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>]
GROUP BY t1.id;
------------------------------------------------------------
------------------------------------------------------------


--- ** Return nº violations **
-- [JOIN]
SELECT COUNT(*)
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

--- Notation
SELECT COUNT(*)
FROM T t1 
JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>];



-- [DISTINCT]
SELECT DISTINCT COUNT(*)
FROM T t1, T t2 
WHERE t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

-- Notation
SELECT DISTINCT COUNT(*)
FROM T t1, T t2
WHERE [where_conditions as <t1.column operator t2.column>];
------------------------------------------------------------
------------------------------------------------------------


-- Return tuples violations as (id1, id2)[]
-- [JOIN]
SELECT t1.id, t2.id
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

-- Notation
SELECT t1.id, t2.id
FROM T t1
JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>];


-- [DISTINCT]
SELECT DISTINCT t1.id, t2.id
FROM T t1, T t2 
WHERE t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

SELECT DISTINCT t1.id, t2.id
FROM T t1, T t2
WHERE [where_conditions as <t1.column operator t2.column>];
------------------------------------------------------------
-- Como fazer isso usando GroupBy e Having ?
------------------------------------------------------------



--- ** Return set (union) of tuples on some DC violation (id)[] **
-- [DISTINCT + JOIN + UNION]

SELECT t1.ID FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate
UNION
  SELECT t2.ID FROM T t1 
  JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
AND t1.Rate < t2.Rate;

-- Notation
SELECT t1.ID FROM t t1 JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>]
UNION
SELECT t2.ID FROM t t1 JOIN T t2
  ON [join_conditions as <t1.column operator t2.column>]
------------------------------------------------------------
------------------------------------------------------------



--- ** Return number of tuples on some DC violation **
SELECT COUNT(*)
FROM (
    SELECT t1.ID FROM T t1 
    JOIN T t2 
    ON t1.State = t2.State 
    AND t1.Salary > t2.Salary 
    AND t1.Rate < t2.Rate
    UNION
    SELECT t2.ID FROM T t1 
    JOIN T t2 
    ON t1.State = t2.State 
    AND t1.Salary > t2.Salary 
    AND t1.Rate < t2.Rate
);

-- Notation
SELECT COUNT(*)
FROM (
  SELECT t1.ID FROM t t1 JOIN T t2
    ON [join_conditions as <t1.column operator t2.column>]
  UNION
  SELECT t2.ID FROM t t1 JOIN T t2
    ON [join_conditions as <t1.column operator t2.column>]
);











-- 428
SELECT t1.id, t2.id
FROM T t1 
JOIN T t2 
  ON t1.State = t2.State 
  AND t1.Salary > t2.Salary 
  AND t1.Rate < t2.Rate;

/*
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐                             
│         PROJECTION        │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│             ID            │                             
│             ID            │                             
└─────────────┬─────────────┘                                                          
┌─────────────┴─────────────┐                             
│         HASH_JOIN         │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│           INNER           │                             
│       State = State       │                             
│        Rate < Rate        ├──────────────┐              
│      Salary > Salary      │              │              
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │              
│         EC: 358654        │              │              
│        Cost: 358654       │              │              
└─────────────┬─────────────┘              │                                           
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             T             ││             T             │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           State           ││           State           │
│           Salary          ││           Salary          │
│            Rate           ││            Rate           │
│             ID            ││             ID            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         EC: 100000        ││         EC: 100000        │
└───────────────────────────┘└───────────────────────────┘  
*/

-- 428
SELECT t1.id, t2.id
FROM T t1, T t2 
  WHERE t1.State = t2.State 
  GROUP BY t1.id, t2.id, t1.Rate, t2.Rate, t1.Salary, t2.Salary 
  Having t1.Rate < t2.Rate AND t1.Salary > t2.Salary;


  /*
  ┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐                             
│         PROJECTION        │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│             ID            │                             
│             ID            │                             
└─────────────┬─────────────┘                                                          
┌─────────────┴─────────────┐                             
│       HASH_GROUP_BY       │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│             #0            │                             
│             #1            │                             
│             #2            │                             
│             #3            │                             
│             #4            │                             
│             #5            │                             
└─────────────┬─────────────┘                                                          
┌─────────────┴─────────────┐                             
│         PROJECTION        │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│             ID            │                             
│             ID            │                             
│            Rate           │                             
│            Rate           │                             
│           Salary          │                             
│           Salary          │                             
└─────────────┬─────────────┘                                                          
┌─────────────┴─────────────┐                             
│         HASH_JOIN         │                             
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             
│           INNER           │                             
│       State = State       │                             
│      Salary > Salary      ├──────────────┐              
│        Rate < Rate        │              │              
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │              
│         EC: 358654        │              │              
│        Cost: 358654       │              │              
└─────────────┬─────────────┘              │                                           
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             T             ││             T             │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           State           ││           State           │
│             ID            ││             ID            │
│            Rate           ││            Rate           │
│           Salary          ││           Salary          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         EC: 100000        ││         EC: 100000        │
└───────────────────────────┘└───────────────────────────┘  
  */






