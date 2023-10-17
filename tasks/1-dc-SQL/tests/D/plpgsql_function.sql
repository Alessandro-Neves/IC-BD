-- Returns if the database contains violations

CREATE TABLE IF NOT EXISTS T (
  id SERIAL PRIMARY KEY,
  Salary DECIMAL,
  State VARCHAR(2),
  Rate DECIMAL
);

CREATE OR REPLACE FUNCTION hasViolations()
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    t1 T%ROWTYPE;
BEGIN
    FOR t1 IN (SELECT * FROM T) LOOP
        IF EXISTS (SELECT 1 FROM T t2 WHERE t1.Rate < t2.Rate) THEN
            RETURN TRUE;
        END IF;
    END LOOP;

    RETURN FALSE;
END;
$$;













INSERT INTO T (Salary, State, Rate) VALUES (2000.0, 'AM', 1.01);
INSERT INTO T (Salary, State, Rate) VALUES (3000.0, 'AM', 2.05);
INSERT INTO T (Salary, State, Rate) VALUES (1000.0, 'AP', 1.01);