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
file_path = '/path/to/yourfile.txt'  # Specify the full file path here

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
                ip_address = line.strip()
                
                # Get the current date and time
                current_date = datetime.now()

                # Insert IP address and date into the specified table
                query = f"INSERT INTO ip (ip, date_added) VALUES (%s, %s)"
                cursor.execute(query, (ip_address, current_date))

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
    upload_ips_to_database(file_path, 'first_table_name')
