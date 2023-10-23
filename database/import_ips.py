import os, psycopg2

from IP_Info import IP_Info
from configparser import ConfigParser


def get_conf() -> tuple[str, str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('DBCredentials', 'user'),
            config_parser.get('DBCredentials', 'password'),
            config_parser.get('DBCredentials', 'database'))

def ips_to_db(ips: list[IP_Info]):
    (user, password, database) = get_conf()
    db_connection = psycopg2.connect(f'dbname={database} user={user} password={password}')
