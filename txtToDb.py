import psycopg2, os, sys
from configparser import ConfigParser

def get_conf() -> tuple[str, str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('CONFIGS', 'workdir_todays'),)

db_params = {
    'host': 'localhost',        # Database host (e.g., localhost)
    'database': '',      # Database name
    'user': '',           # Database username
    'password': ''    # Database password
}

file_path = '/home/letmeout/git/let-me-out/example.txt' 

def read_data_from_txt():
    data_from_txt = list()
    values = list()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains an IP address
                values = line.strip().split('|')
                data_from_txt.append(values)
        return data_from_txt
    except Exception as ex:
        print("ERROR: In opening and importing data from the txt file.")
        print(ex)
        sys.exit(1)


def update_ip_table(data_list):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    try:
        for data in data_list:
            query_table1 = "INSERT INTO ip (ip) VALUES (%s)" 
            cursor.execute(query_table1, (data[0],))
        connection.commit()
        if connection:
            cursor.close()
            connection.close()

    except Exception as ex:
        print("ERROR: Bigger list is not opened")
        print(ex)
        sys.exit(1)
        

def update_ip_data_table(data_list):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    import_ip_table = "SELECT * FROM ip;"
    cursor.execute(import_ip_table)
    ip_table = cursor.fetchall()

    f_key = list()

    try:
        for data in data_list:
            for ip in ip_table:
                if data[0] == ip[1]:
                    f_key.append(ip[0])
                
    except Exception as ex:
        print("ERROR")
        print(ex)
        sys.exit(1)

    i = 0
    for d in data_list:
        d[0] = f_key[i]
        i +=1

    for data in data_list:
            query_table2 = "INSERT INTO ip_data (ip_id, detection_day, danish_network, abuse_confidence_score, usage_type, isp, domain, country_code, total_reports, num_distinct_users, is_tor, is_whitelisted, categories, reported_at, last_reported_at, undetected, harmless, suspicious, malicious, reputation) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(query_table2, data)

    connection.commit()
    if connection:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    #global working_directory
    #(working_directory) = get_conf()
    from_txt = read_data_from_txt()
    update_ip_table(from_txt)
    update_ip_data_table(from_txt)