DROP TABLE IF EXISTS r;
CREATE TABLE r (id INT PRIMARY KEY, val VARCHAR(6));
INSERT INTO r VALUES (100, 'aaa'), (101, 'bbb'), (102, 'ccc');
SELECT * FROM r;

SELECT r.ctid, r.* from r;

DELETE FROM r WHERE id = 101;
SELECT r.ctid, r.* from r;

INSERT INTO r VALUES (103, 'ddd'), (104, 'eee');
SELECT r.ctid, r.* from r;

VACUUM FULL r;
SELECT r.ctid, r.* from r;

SELECT r.ctid, r.* FROM r WHERE ctid = '(0,2)';