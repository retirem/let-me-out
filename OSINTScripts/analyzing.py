import requests, sys, logging, json

from IP_Info import IP_Info
from argparse import ArgumentParser


virustotal_api_key = 'REPLACE_API_KEY'
ipqualityscore_api_key = 'REPLACE_API_KEY'

def configure_logging(working_directory: str) -> None:
    log_path: str = working_directory + '/analyze.log'
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def parse_arguments() -> str:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-w', '--workdir', type=str, help='Working directory path.', required=True)
    args = parser.parse_args()
    return str(args.workdir)

def read_ips(working_directory: str) -> list[IP_Info]:
    filepath: str = working_directory + '/blocked_ips_networks.txt'
    logging.info('Reading IPs from file: ' + filepath)
    with open(filepath, 'r') as ip_file:
        return list(map(lambda read_ip: IP_Info(read_ip), map(lambda ip: ip.strip(), ip_file.readlines())))

def virustotal(ips: list[IP_Info]) -> None:
    logging.info('Starting analyzing IPs with VirusTotal...')
    headers = {'x-apikey': virustotal_api_key}
    for ip in ips:
        url: str = f'https://www.virustotal.com/api/v3/ip_addresses/{ip.ip}'
        response: requests.Response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data = data.get('data')

            ip.ip = data.get('id')
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
        url: str = f'https://ipqualityscore.com/api/json/ip/{ipqualityscore_api_key}/{ip}'
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


if __name__ == '__main__':
    working_directory: str = parse_arguments()
    configure_logging(working_directory=working_directory)
    ips: list[IP_Info] = read_ips(working_directory=working_directory)
    virustotal(working_directory=working_directory, ips=ips)
    ipqualityscore(ips=ips)
