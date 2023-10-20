import requests, sys, logging

from IP_Info import IP_Info
from argparse import ArgumentParser

# This script will provide you with detailed information about each IP address, including its reputation, whois information, and the results from various antivirus engines.
virustotal_api_key = 'REPLACE_API_KEY'
ipqualityscore_api_key = 'REPLACE_API_KEY'

def configure_logging(working_directory: str) -> None:
    log_path: str = working_directory + '/analyze.log'
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def parse_arguments() -> (str, str):
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='Path to file containing IPs.', required=True)
    parser.add_argument('-w', '--workdir', type=str, help='Working directory path.', required=True)
    args = parser.parse_args()
    return (args.path, args.workdir)

def read_ips(filepath: str) -> list[IP_Info]:
    logging.info('Reading IPs from file: ' + filepath)
    with open(filepath, 'r') as ip_file:
        return map(lambda read_ip: IP_Info(read_ip), map(lambda ip: ip.strip(), ip_file.readlines()))

def virustotal(ips: list[IP_Info]) -> None:
    logging.info('Starting analyzing IPs with VirusTotal...')

    headers = {'x-apikey': virustotal_api_key}
    for ip in ips:
        url: str = f'https://www.virustotal.com/api/v3/ip_addresses/{ip.ip_address}'
        response: requests.Response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            data = data.get('data')
            analyzed_ip: IP_Info = IP_Info()

            # Basic IP information
            analyzed_ip.ip = data.get('id')
            analyzed_ip.network = data.get('attributes').get('network')

            analyzed_ip.virustotal['reputation'] = data.get('attributes').get('reputation')

            last_analysis_stats = data.get('attributes').get('last_analysis_stats')
            analyzed_ip.virustotal['harmless_count'] = last_analysis_stats.get('harmless')
            analyzed_ip.virustotal['suspicious_count'] = last_analysis_stats.get('suspicious')
            analyzed_ip.virustotal['malicious_count'] = last_analysis_stats.get('malicious')
            analyzed_ip.virustotal['undetected_count'] = last_analysis_stats.get('undetected')
        else:
            logging.error(f'VirusTotal API response gave error for IP: {ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with VirusTotal.')

def ipqualityscore(ips: list[IP_Info]) -> None:
    logging.info('Starting analyzing IPs with IPQualityScore...')

    for ip in ips:
        url: str = f'https://ipqualityscore.com/api/json/ip/{ipqualityscore_api_key}/{ip}'
        response: requests.Response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            ip.ipqualityscore['is_proxy'] = data.get('proxy')
            ip.ipqualityscore['is_vpn'] = data.get('vpn')
            ip.ipqualityscore['is_tor'] = data.get('tor')
            ip.ipqualityscore['is_bot'] = data.get('is_bot')

            ip.ipqualityscore['risk_score'] = data.get('risk_score')

            ip.ipqualityscore['geolocation'] = {
                'city': data.get('city'),
                'region': data.get('region'),
                'country': data.get('country')
            }
        else:
            logging.error(f'IPQualityScore API response gave error for IP: {ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with IPQualityScore.')


if __name__ == '__main__':
    (ip_file_path, workdir): str = parse_arguments()
    configure_logging(working_directory=workdir)
    ips: list[IP_Info] = read_ips(filepath=ip_file_path)
    virustotal(ips=ips)
    ipqualityscore(ips=ips)
