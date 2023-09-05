import duckdb
import pandas
import time

duck_conn = duckdb.connect() # type: ignore

# data = duckconn.execute(
#   """
#     SELECT * 
#     FROM spotify_170k.csv 
#     LIMIT 10
#   """
# ).df()

data = pandas.read_csv("spotify_170k.csv")
duck_conn.execute("CREATE TABLE t as SELECT * FROM 'spotify_170k.csv'")
duck_table = duck_conn.table('t')
# T = duckdb.register("T", data) # type: ignore


# t = T.table("T")
# table = duckconn.table()

# WHERE duration_ms = 314933 AND release_date = 1968

cur_time = time.monotonic()
r1 = duck_conn.execute("SELECT * FROM T WHERE duration_ms = 314933 AND release_date = 1968 AND year = 1968").df()
# r1 = duck_table.filter(data, "durantion_ms == 158648") # type: ignore
end_time = time.monotonic()

print(end_time - cur_time)

cur_time = time.monotonic()
r2 = data[(data['duration_ms'] == 314933) & (data['release_date'] == '1968') & (data['year'] == 1968)]
end_time = time.monotonic()

print(end_time - cur_time)

print()
# print(len(r1))
# print(len(r2))

print(r1)
print(r2)


# print(duckdb.filter(test_df, 'i > 1'))
# print(duckdb.project(test_df, 'i +1'))
# print(duckdb.order(test_df, 'j'))
# print(duckdb.limit(test_df, 2))

# print(duckdb.aggregate(test_df, "sum(i)"))
# print(duckdb.distinct(test_df))

# # when chaining only the first call needs to include the data frame parameter
# print(duckdb.filter(test_df, 'i > 1').project('i + 1').order('j').limit(2))