import os, json

from configparser import ConfigParser
from ip_info import IP_Info


def get_conf():
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return config_parser.get('CONFIGS', 'workdir_todays')

def read_ips():
    analyzed_ips_path: str = os.path.join(working_directory, 'analyzed_ips.json')
    with open(analyzed_ips_path, 'r') as ip_file:
        analyzed_ips_json: dict = json.load(ip_file)
        


if __name__ == '__main__':
    global working_directory
    working_directory = get_conf()

    ips: list[IP_Info] = read_ips()