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

def abuseipdb(ips):
    logging.info('Starting analyzing IPs with AbuseIPDB...')

    # Define your AbuseIPDB API key
    abuseipdb_api_key = api_handler.get_abuseIPDB_key()

    results = []  # Create a list to store the results as JSON objects

    for ip in ips:
        url = f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip.ip}&maxAgeInDays=365'

        # Set up headers with your API key
        headers = {
            'Accept': 'application/json',
            'Key': abuseipdb_api_key,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json().get('data')
            if data:
                # Create a JSON structure to store the information
                ip_info = {
                    'ip': ip.ip,
                    'isPublic': data.get('isPublic'),
                    'ipVersion': data.get('ipVersion'),
                    'isWhitelisted': data.get('isWhitelisted'),
                    'abuseConfidenceScore': data.get('abuseConfidenceScore'),
                    'countryCode': data.get('countryCode'),
                    'countryName': data.get('China'),
                    'usageType': data.get('usageType'),
                    'isp': data.get('isp'),
                    'domain': data.get('domain'),
                    'hostnames': data.get('hostnames'),
                    'isTor': data.get('isTor'),
                    'totalReports': data.get('totalReports'),
                    'numDistinctUsers': data.get('numDistinctUsers'),
                    'lastReportedAt': data.get('lastReportedAt'),
                }

                reports = data.get('reports')

                if reports:
                    ip_info = {
                        'reportedAt': get.data('reportedAt'),
                        'comment': get.data('comment'),
                        'categories': get.data('categories'),
                        'reporterId': get.data('reporterId'),
                        'reporterCountryCode': get.data('reporterCountryCode'),
                        'reporterCountryName': get.data('reporterCountryName'),
                    }

                results.append(ip_info)  # Append the JSON object to the results list

            else:
                logging.warning(f'No AbuseIPDB data available for IP: {ip.ip}')
        else:
            logging.error(f'AbuseIPDB API response gave error for IP: {ip.ip}, Status code: {response.status_code}')


def export_analyzed_ips_as_txt(ips: list[IP_Info]) -> None:
    analyzed_path: str = os.path.join(working_directory, 'analyzed_ips.txt')
    with open(analyzed_path, 'w') as output_file:
        for ip in ips:
            output_line = f"{ip.ip}, {ip.network}, {ip.virustotal['reputation']}, {ip.virustotal['harmless_count']}, {ip.virustotal['suspicious_count']}, {ip.virustotal['malicious_count']}, {ip.virustotal['undetected_count']},{ip.abuseipdb_data['ip']},{ip.abuseipdb_data['isPublic']},{ip.abuseipdb_data['countryCode']}, {ip.abuseipdb_data['isp']}, {ip.abuseipdb_data['domain']}, {ip.abuseipdb_data['totalReports']}, {ip.abuseipdb_data['lastReportedAt']} "

    output_file.write(output_line + "\n")

    logging.info('Created text file with analyzed IPs at: ' + analyzed_path)


if __name__ == '__main__':
    global working_directory, api_handler
    (working_directory, virustotal_api_keys, abuseIPDB_api_keys) = get_conf()
    api_handler = APIHandler(virustotal_keys=virustotal_api_keys, abuseIPDB_keys=abuseIPDB_api_keys)

    configure_logging()
    ips: list[IP_Info] = read_ips()
    virustotal(ips=ips)
    abuseipdb(ips=ips)

    export_analyzed_ips_as_txt(ips=ips)
