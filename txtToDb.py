import os, psycopg2, datetime
from configparser import ConfigParser

def get_conf() -> tuple[str, str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('DBCredentials', 'user'),
            config_parser.get('DBCredentials', 'password'),
            config_parser.get('DBCredentials', 'database'))


# Function to upload IP addresses to the specified table in the database
def upload_ips_to_database(file_path, ip):
    try:
        # Establish a database connection
        (user, password, database) = get_conf()
        db_connection = psycopg2.connect(f'dbname={database} user={user} password={password}')
        cursor = db_connection.cursor()


        # Open the text file and read IP addresses line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains an IP address
                ip_address = line.strip()

                # Get the current date and time
                current_date = datetime.now()

                # Insert IP address and date into the specified table
                query = f"INSERT INTO {ip} (ip, date_added) VALUES (%s, %s)"
                cursor.execute(query, (ip_address, current_date))

        # Commit the transaction and close the connection
        db_connection.commit()
        print(f"IP addresses uploaded to {ip} table successfully!")

    except psycopg2.Error as e:
        print(f"Error: Unable to upload IP addresses to {ip} table.")
        print(e)

    finally:
        # Close the database connection
        if db_connection:
            cursor.close()
            db_connection.close()

# Example usage
if __name__ == "__main__":
    file1_path = input("/example.txt")

    # Upload IP addresses to the first table
    upload_ips_to_database(file1_path, 'first_table_name')
