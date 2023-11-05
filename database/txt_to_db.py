import psycopg2, os, sys, logging

from shutil import which
from configparser import ConfigParser
from subprocess import run, PIPE, CompletedProcess

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
            cursor.execute(insert_query, (ip_values[0], ip_values[0],))
            id: int = cursor.fetchone()

            # If ip is already existing in the db, we need the id of it
            if id is None:
                cursor.execute(id_query, (ip_values[0],))
                id = cursor.fetchone()
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

def update_ip_data_table(ip_values_with_db_ids: dict[int, list[str]]) -> None:
    try:
        connection = psycopg2.connect(host='localhost',
                                    database=db_credentials.get('database'),
                                    user=db_credentials.get('user'),
                                    password=db_credentials.get('password'))
        cursor = connection.cursor()

        insert_query: str = '''INSERT INTO ip_data (ip_id, detection_day, danish_network, abuse_confidence_score, usage_type, isp, domain, country_code, total_reports, num_distinct_users, is_tor, is_whitelisted, categories, reported_at, last_reported_at, undetected, harmless, suspicious, malicious, reputation)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

        for ip_id, ip_values in ip_values_with_db_ids.items():
            cursor.execute(insert_query, (ip_id, *list(map(lambda value: None if value == 'None' else value, ip_values))[1:]))

        connection.commit()
        cursor.close()
        if connection is not None:
            connection.close()
    except Exception as ex:
        logging.error('Error during saving data to ip_data table: ' + str(ex.args))
        if connection is not None:
            connection.close()
        print('Exiting now...')
        sys.exit(1)

def check_command_availability(command: str) -> None:
    logging.info(f'Checking for {command} command availability...')
    if which(command) is None:
        logging.error(f'{command} command is not available in the $PATH.')
        sys.exit(1)
    logging.info(f'{command} command is available.')

def create_db_backup() -> None:
    check_command_availability('pg_dump')
    result: CompletedProcess = run(['pg_dump', 'letmeout_cyber1', '-f', os.path.join(working_directory, 'db_backup.sql')], stderr=PIPE, universal_newlines=True)
    if result.returncode != 0:
        logging.error('An error happened during executing pg_dump command: ' + str(result.stderr))
        print('Exiting now...')
        sys.exit(1)
    logging.info('Created database backup in daily working directory.')

if __name__ == '__main__':
    global working_directory, db_credentials
    (working_directory, db_credentials) = get_conf()

    configure_logging()

    ip_values_containered: list[list[str]] = read_data_from_txt()
    ip_values_with_db_ids: dict[int, list[str]] = update_ip_table(ip_values_containered=ip_values_containered)
    update_ip_data_table(ip_values_with_db_ids=ip_values_with_db_ids)
    create_db_backup()
