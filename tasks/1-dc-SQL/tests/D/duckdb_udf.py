import pandas as pd
import duckdb

def query(state, salary, rate):
  return f"SELECT * FROM T t WHERE '{state}' = t.State AND {salary} > t.Salary AND {rate} < t.Rate;"

df = pd.read_csv('tax_100k_noisy_0.5.csv')

con = duckdb.connect(database=':memory:')
con.register('T', df)

rows = con.execute("SELECT * FROM T;").fetchall()

for row in rows:
  q = query(row[3], row[6], row[7])
  res = con.execute(q).fetchone()
  if res:
    print(res[0])
    break

con.close()