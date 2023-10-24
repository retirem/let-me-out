import requests, sys, logging, os, json

from IP_Info import IP_Info
from api_handler import APIHandler
from configparser import ConfigParser


def get_conf() -> tuple[str, str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('CONFIGS', 'workdir_todays'),
            config_parser.get('CONFIGS', 'virustotal_api_keys').split(','),
            config_parser.get('CONFIGS', 'abuseIPDB_api_keys').split(','))

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

# def abuseIPDBscore(ips: list[IP_Info]) -> None:
#     logging.info('Starting analyzing IPs with abuseIPDBscore...')

#     for ip in ips:
#         url: str = f'https://abuseIPDBscore.com/api/json/ip/{api_handler.get_abuseIPDBscore_key()}/{ip}'
#         response: requests.Response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()

#             ip.abuseIPDBscore = {
#                 'is_proxy': data.get('proxy'),
#                 'is_vpn': data.get('vpn'),
#                 'is_tor': data.get('tor'),
#                 'is_bot': data.get('is_bot'),
#                 'risk_score': data.get('risk_score'),
#                 'geolocation': {
#                     'city': data.get('city'),
#                     'region': data.get('region'),
#                     'country': data.get('country'),
#                 },
#             }
#         else:
#             logging.error(f'abuseIPDBscore API response gave error for IP: {ip.ip}, Status code: {response.status_code}')

#     logging.info('Finished analyzing IPs with abuseIPDBscore.')

def abuseipdb(ips):
    logging.info('Starting analyzing IPs with AbuseIPDB...')

    # Define your AbuseIPDB API key
    abuseipdb_api_key = api_handler.get_abuseIPDB_key()

    for ip in ips:
        url = f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=30'

        # Set up headers with your API key
        headers = {
            'Key': abuseipdb_api_key,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                # Access the data in the response (e.g., the abuse confidence score)
                confidence_score = data['data']['abuseConfidenceScore']
                categories = data['data']['categories']
                # Add the AbuseIPDB data to the IP_Info object
                ip.abuseipdb = {
                    'confidence_score': confidence_score,
                    'categories': categories
                }
            else:
                logging.warning(f'No AbuseIPDB data available for IP: {ip}')
        else:
            logging.error(f'AbuseIPDB API response gave error for IP: {ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with AbuseIPDB.')

def export_analyzed_ips(ips: list[IP_Info]) -> None:
    analyzed_path: str = os.path.join(working_directory, 'analyzed_ips.json')
    with open(analyzed_path, 'w') as output_file:
        json.dump([ip.__dict__ for ip in ips], output_file, indent=4)
    logging.info('Created JSON file with analyzed IPs at: ' + analyzed_path)


if __name__ == '__main__':
    global working_directory, api_handler
    (working_directory, virustotal_api_keys, abuseIPDB_api_keys) = get_conf()
    api_handler = APIHandler(virustotal_keys=virustotal_api_keys, abuseIPDB_keys=abuseIPDB_api_keys)

    configure_logging()
    ips: list[IP_Info] = read_ips()
    virustotal(ips=ips)
    abuseIPDBscore(ips=ips)

    export_analyzed_ips(ips=ips)
