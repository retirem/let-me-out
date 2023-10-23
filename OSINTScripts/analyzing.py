import requests, sys, logging, os, json

from IP_Info import IP_Info
from api_handler import APIHandler
from configparser import ConfigParser
from database.import_ips import ips_to_db


def get_conf() -> tuple[str, str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('CONFIGS', 'workdir_todays'),
            config_parser.get('CONFIGS', 'virustotal_api').split(','),
            config_parser.get('CONFIGS', 'ipqualityscore_api').split(','))

def configure_logging() -> None:
    log_path: str = os.path.join(working_directory, 'analyze.log')
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def read_ips() -> list[IP_Info]:
    ip_path: str = os.path.join(working_directory, 'blocked_ips_networks.txt')
    logging.info('Reading IPs from file: ' + ip_path)
    with open(ip_path, 'r') as ip_file:
        return list(map(lambda read_ip: IP_Info(read_ip), map(lambda ip: ip.strip(), ip_file.readlines())))

def virustotal(ips: list[IP_Info]) -> None:
    logging.info('Starting analyzing IPs with VirusTotal...')
    headers = {'x-apikey': api_handler.get_virustotal_key()}
    for ip in ips:
        url: str = f'https://www.virustotal.com/api/v3/ip_addresses/{ip.ip}'
        response: requests.Response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json().get('data')

            ip.network = data.get('attributes').get('network')

            last_analysis_stats = data.get('attributes').get('last_analysis_stats')
            ip.virustotal = {
                'reputation': data.get('attributes').get('reputation'),
                'harmless_count': last_analysis_stats.get('harmless'),
                'suspicious_count': last_analysis_stats.get('suspicious'),
                'malicious_count': last_analysis_stats.get('malicious'),
                'undetected_count': last_analysis_stats.get('undetected'),
            }
        else:
            logging.error(f'VirusTotal API response gave error for IP: {ip.ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with VirusTotal.')

def ipqualityscore(ips: list[IP_Info]) -> None:
    logging.info('Starting analyzing IPs with IPQualityScore...')

    for ip in ips:
        url: str = f'https://ipqualityscore.com/api/json/ip/{api_handler.get_ipqualityscore_key()}/{ip}'
        response: requests.Response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            ip.ipqualityscore = {
                'is_proxy': data.get('proxy'),
                'is_vpn': data.get('vpn'),
                'is_tor': data.get('tor'),
                'is_bot': data.get('is_bot'),
                'risk_score': data.get('risk_score'),
                'geolocation': {
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country': data.get('country'),
                },
            }
        else:
            logging.error(f'IPQualityScore API response gave error for IP: {ip.ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with IPQualityScore.')

def export_analyzed_ips(ips: list[IP_Info]) -> None:
    analyzed_path: str = os.path.join(working_directory, 'analyzed_ips.json')
    with open(analyzed_path, 'w') as output_file:
        json.dump([ip.__dict__ for ip in ips], output_file, indent=4)
    logging.info('Created JSON file with analyzed IPs at: ' + analyzed_path)


if __name__ == '__main__':
    global working_directory, api_handler
    (working_directory, virustotal_api_keys, ipqualityscore_api_keys) = get_conf()
    api_handler = APIHandler(virustotal_keys=virustotal_api_keys, ipqualityscore_keys=ipqualityscore_api_keys)

    configure_logging()
    ips: list[IP_Info] = read_ips()
    virustotal(ips=ips)
    ipqualityscore(ips=ips)

    export_analyzed_ips(ips=ips)

    ips_to_db(ips=ips)
