import psycopg2

#EXAMPLE to introduce text to DB:

# Define your database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"  # PostgreSQL default port
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Sample data from a text file (you should replace this with your data parsing logic)
sample_data = {
    "ip": "192.168.1.1",
    "detection_day": "2023-10-27",
}

# SQL statement to insert data into the 'ip' table
insert_ip_data = """
INSERT INTO ip (ip, detection_day)
VALUES (%(ip)s, %(detection_day)s);
"""

# Execute the SQL statement with the sample data
cursor.execute(insert_ip_data, sample_data)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
