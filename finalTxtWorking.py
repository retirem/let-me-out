import psycopg2
from datetime import datetime

# Database connection parameters
db_params = {
    'host': 'localhost',        # Database host (e.g., localhost)
    'database': 'postgres',      # Database name
    'user': 'myuser',           # Database username
    'password': 'mypassword'    # Database password
}

# File path to the text file containing IP addresses
file_path = '/home/kali/projects/let-me-out/example.txt'  # Specify the full file path here

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
                values = line.strip(|)

             

                # Get the current date and time
                current_date = datetime.now()

                # Insert IP address and date into the specified table
                query_table1 = f"INSERT INTO ip (ip) VALUES (inet %s)"
                query_table2 = f"INSERT INTO ip_data (danish_network, current_date, virus_reputation, virus_harmless, virus_suspicious, virus_malicious, virus_undetected, abuse_is_public, abuse_country_code, abuse_isp, abuse_domain, abuse_totalReports,abuse_last_reported_at) VALUES (cidr %s, date %s, integer %s, integer %s, integer %s, integer %s, integer %s, integer %s, boolean %s, text %s, text %s, text %s, integer %s, text %s)"
                
                # cursor.execute(query, (ip_address, current_date))
		cursor.execute(query_table1, (values[0],))
		cursor.execute(query_table2, (values[1],))
		
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
