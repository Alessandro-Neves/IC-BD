CREATE TABLE T AS SELECT * FROM 'employees_40000.csv';
EXPLAIN SELECT t1.id as id1, t2.id as id2  FROM T t1 JOIN T t2  ON t1.salary > t2.salary  AND t1.hiring_year > t2.hiring_year  AND t1.id <> t2.id;

CREATE TABLE Tax AS SELECT * FROM 'tax_1000000.csv';
SELECT COUNT(*) as result FROM Tax t1 JOIN Tax t2 ON t1.State = t2.State AND t1.Salary > t2.Salary AND t1.Rate < t2.Rate;


CREATE TABLE Tax AS SELECT * FROM 'tax_10k.csv';


CREATE TABLE T AS SELECT * FROM 'tax_1k_1_noisy.csv';
CREATE SEQUENCE T_SEQ START 1;
ALTER TABLE T ADD COLUMN ID INT;
UPDATE T SET ID = nextval('T_SEQ');

DROP TABLE T; DROP SEQ SEQ_T;