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
    ip inet NOT NULL,
    detection_day DATE NOT NULL
);
"""

create_ip_data_table = """
CREATE TABLE IF NOT EXISTS ip_data (
    data_id SERIAL PRIMARY KEY,
    danish_network cidr NOT NULL,
    abuse_confidence_score INTEGER NOT NULL,
    usage_type TEXT NOT NULL,
    isp TEXT NOT NULL,
    domain TEXT NOT NULL,
    total_reports INTEGER NOT NULL,
    num_distinct_users INTEGER NOT NULL,
    is_tor BOOLEAN NOT NULL,
    is_whitelisted BOOLEAN NOT NULL,
    category_id INTEGER,
    reported_at DATE NOT NULL,
    last_reported_at DATE,
    virustotal VARCHAR(255)
);
"""

create_category_id_data_table = """
CREATE TABLE IF NOT EXISTS category_id_data (
    data_id SERIAL PRIMARY KEY,
    dns_compromise_id INTEGER,
    dns_poisoning_id INTEGER,
    fraud_orders_id INTEGER,
    ddos_attack_id INTEGER,
    ftp_brute_force_id INTEGER,
    ping_of_death_id INTEGER,
    phishing_id INTEGER,
    fraud_voip_id INTEGER,
    open_proxy_id INTEGER,
    web_spam_id INTEGER,
    email_spam_id INTEGER,
    blog_spam_id INTEGER,
    vpn_ip_id INTEGER,
    port_scan_id INTEGER,
    hacking_id INTEGER,
    sql_injection_id INTEGER,
    spoofing_id INTEGER,
    brute_force INTEGER,
    bad_web_bot INTEGER,
    exploited_host INTEGER,
    web_app_attack INTEGER,
    ssh INTEGER,
    iot_targeted INTEGER
);
"""

# Execute the SQL statements
cursor.execute(create_ip_table)
cursor.execute(create_ip_data_table)
cursor.execute(create_category_id_data_table)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
