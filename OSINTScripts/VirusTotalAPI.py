import requests, sys, logging

from argparse import ArgumentParser

# This script will provide you with detailed information about each IP address, including its reputation, whois information, and the results from various antivirus engines.
api_key = 'REPLACE_API_KEY'

class IP_Info:
    def __init__(self) -> None:
        self.ip: str = ''
        self.network: str = ''
        self.reputation: int = 0
        self.harmless_count: int = 0
        self.malicious_count: int = 0
        self.suspicious_count: int = 0
        self.undetected_count: int = 0


def configure_logging(working_directory: str) -> None:
    log_path: str = working_directory + '/virustotal.log'
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def parse_arguments() -> (str, str):
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='Path to file containing IPs.', required=True)
    parser.add_argument('-w', '--workdir', type=str, help='Working directory path.', required=True)
    args = parser.parse_args()
    return (args.path, args.workdir)

def read_ips(filepath: str) -> list[str]:
    logging.info("Reading IPs from file: " + filepath)
    with open(filepath, 'r') as ip_file:
        return map(lambda ip: ip.strip(), ip_file.readlines())

def analyze_ips(ips: list[str]) -> list[IP_Info]:
    logging.info('Starting analyzing IPs with VirusTotal...')
    analyzed_ips: list[IP_Info] = []

    headers = {'x-apikey': api_key}
    for ip in ips:
        url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            analyzed_ip: IP_Info = IP_Info()

            # Basic IP information
            analyzed_ip.ip = data['data']['id']
            analyzed_ip.network = data['data']['attributes']['network']
            analyzed_ip.reputation = data['data']['attributes']['reputation']

            last_analysis_stats = data['data']['attributes']['last_analysis_stats']
            analyzed_ip.harmless_count = last_analysis_stats['harmless']
            analyzed_ip.suspicious_count = last_analysis_stats['suspicious']
            analyzed_ip.malicious_count = last_analysis_stats['malicious']
            analyzed_ip.undetected_count = last_analysis_stats['undetected']

            analyzed_ips.append(analyzed_ip)
        else:
            logging.error(f'API response gave error for IP: {ip}, Status code: {response.status_code}')

    logging.info('Finished analyzing IPs with VirusTotal.')
    return analyzed_ips

if __name__ == "__main__":
    (ip_file_path, workdir): str = parse_arguments()
    configure_logging(working_directory=workdir)
    ips: list[str] = read_ips(filepath=ip_file_path)
    analyzed_ips: list[IP_Info] = analyze_ips(ips=ips)
