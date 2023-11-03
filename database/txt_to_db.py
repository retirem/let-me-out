import psycopg2, os, sys, logging
from configparser import ConfigParser

def get_conf() -> tuple[str, dict[str, str]]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('CONFIGS', 'workdir_todays'),
            dict(config_parser.items('DBCredentials')))

def configure_logging() -> None:
    log_path: str = os.path.join(working_directory, 'database_insert.log')
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def read_data_from_txt() -> list[list[str]]:
    try:
        with open(os.path.join(working_directory, 'analyzed_ips.txt'), 'r') as file: # FIXME filename might be wrong
            return list(map(lambda line: line.strip().split('|'), file.readlines()))
    except Exception as ex:
        logging.error("Error during opening and reading analyzed_ips.txt: " + str(ex.args))
        print('Exiting now...')
        sys.exit(1)

def update_ip_table(ip_values_containered: list[list[str]]) -> dict[int, list[str]]:
    ip_values_with_db_ids: dict[int, list[str]] = {}
    try:
        connection = psycopg2.connect(host='localhost', 
                                    database=db_credentials.get('database'),
                                    user=db_credentials.get('user'),
                                    password=db_credentials.get('password'))

        cursor = connection.cursor()
        insert_query: str = 'INSERT INTO ip (ip) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM ip WHERE ip = %s) RETURNING ip_id;'
        id_query: str = 'SELECT ip_id FROM ip WHERE ip = %s;'
        for ip_values in ip_values_containered:
            cursor.execute(insert_query, (ip_values[0]))
            id: int = cursor.fetchone()[0]

            # If ip is already existing in the db, we need the id of it
            if id is None:
                cursor.execute(id_query, (ip_values[0]))
                id = cursor.fetchone()[0]
            ip_values_with_db_ids[id] = ip_values

        connection.commit()
        cursor.close()
        if connection is not None:
            connection.close()
        return ip_values_with_db_ids
    except Exception as ex:
        logging.error('Error during saving IPs to ip table: ' + str(ex.args))
        if connection is not None:
            connection.close()
        print('Exiting now...')
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
    global working_directory, db_credentials
    (working_directory, db_credentials) = get_conf()

    configure_logging()

    ip_values_containered: list[list[str]] = read_data_from_txt()
    ip_values_with_db_ids: dict[int, list[str]] = update_ip_table(ip_values_containered=ip_values_containered)
    update_ip_data_table(from_txt) # TODO
