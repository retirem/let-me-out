import os, json

from configparser import ConfigParser
from OSINTScripts.IP_Info import IP_Info


def get_conf() -> tuple[str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('DBCredentials', 'user'),
            config_parser.get('DBCredentials', 'password'))

def ips_to_db(ips: list[IP_Info]):
    (user, password) = get_conf()
