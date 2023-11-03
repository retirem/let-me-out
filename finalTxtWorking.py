import psycopg2
from datetime import datetime

# Database connection parameters
db_params = {
    'host': 'localhost',        # Database host (e.g., localhost)
    'database': '',      # Database name
    'user': '',           # Database username
    'password': ''    # Database password
}

# File path to the text file containing IP addresses
file_path = '/home/letmeout/git/let-me-out/example.txt'  # Specify the full file path here

# Function to upload IP addresses to the specified table in the database
def upload_ips_to_database(file_path, table_name):
    try:
        # Establish a database connection
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Open the text file and read IP addresses line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains an IP address
                values = line.strip().split('|')



 	# Check if there are enough elements in the values list
                if len(values) >= 19:

                    # Insert IP address and date into the specified table
                    query_table1 = "INSERT INTO ip (ip) VALUES (%s)"
                    query_table2 = "INSERT INTO ip_data (detection_day, danish_network, usage_type, isp, domain, country_code, total_reports, num_distinct_users, is_tor, is_whitelisted, categories, reported_at, last_reported_at, undetected, harmless, suspicious, malicious, reputation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"



                    # Pad with None values and replace them with 'NULL'
                    values = [value if value is not None else None for value in values] + [None] * (20 - len(values))


                    # values = [None if value == 'None' else value for value in values]

                    # Insert IP address and date into the specified table
                    cursor.execute(query_table1, (values[0],))

                    # Insert data into 'ip_data' table
                    cursor.execute(query_table2, (values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13], values[14], values[15], values[16], values[17], values[18] ))

                else:
                    print(f"Skipping line due to insufficient values: {line}")


        # Commit the transaction and close the connection
        connection.commit()
        print(f"IP addresses uploaded to {table_name} table successfully!")

    except psycopg2.Error as e:
        print(f"Error: Unable to upload IP addresses to {table_name} table.")
        print(e)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()

# Example usage
if __name__ == "__main__":
    # Upload IP addresses to the first table
    upload_ips_to_database(file_path, 'ip')
