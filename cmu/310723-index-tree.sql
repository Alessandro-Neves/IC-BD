-- [POSTGRES]

-- create a index based on b+-tree
CREATE INDEX idx_email_tree ON emails USING BTREE (email);

-- create a index based on hash table
CREATE INDEX idx_emails_hash ON email USING HASH (email);

-- test case pipeline
EXPLAIN SELECT MIN(email) FROM emails;
EXPLAIN SELECT * FROM emails WHERE email LIKE 'foo%';

-- query where postgres uses sequential scan
SELECT * FROM emails WHERE email > 'andy@';

-- query where postgres uses hash table index
SELECT * FROM emails WHERE email = '00@00.000' OR email = 'azevedo.raphaell@hotmail.com';

-- query where postgres uses btree index
SELECT * FROM email WHERE email > 'zzzz';