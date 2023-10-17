import psycopg2

# PostgreSQL database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'root',
    'user': 'root',
    'password': 'root'
}

# CSV file path
csv_file = 'tax_100k_noisy_0.5.csv'

# PostgreSQL table name
table_name = 'Tax'

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Execute the COPY command to import data from the CSV file
copy_sql = f"""
    COPY {table_name} FROM stdin WITH CSV HEADER
    DELIMITER as ','
    """
with open(csv_file, 'r') as f:
    cursor.copy_expert(sql=copy_sql, file=f)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()