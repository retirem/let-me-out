import psycopg2

# Database connection parameters
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

# Define SQL statements to create tables
create_ip_table = """
CREATE TABLE IF NOT EXISTS ip (
    ip_id SERIAL PRIMARY KEY,
    ip inet NOT NULL
    
);
"""

create_ip_data_table = """
CREATE TABLE IF NOT EXISTS ip_data (
    data_id SERIAL PRIMARY KEY,
    danish_network cidr NOT NULL,
    detection_day DATE NOT NULL,
    virus_reputation INTEGER NOT NULL,
    virus_harmless INTEGER NOT NULL,
    virus_suspicious INTEGER NOT NULL,
    virus_malicious INTEGER NOT NULL,
    virus_undetected INTEGER NOT NULL,
    abuse_is_public BOOLEAN NOT NULL,
    abuse_country_code TEXT NOT NULL,
    abuse_isp TEXT NOT NULL,
    abuse_domain TEXT NOT NULL,
    abuse_total_reports INTEGER NOT NULL,
    abuse_last_reported_at INTEGER NOT NULL
);
"""


# Execute the SQL statements
cursor.execute(create_ip_table)
cursor.execute(create_ip_data_table)


# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
