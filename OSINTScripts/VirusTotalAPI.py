import requests
import json

# This script will provide you with detailed information about each IP address, including its reputation, whois information, and the results from various antivirus engines.
api_key = 'XXXXXXXXX'



# List of IPs to check
ips_to_check = ['91.240.189.0', '91.240.189.1']  # Add all IPs you want to analyze

for ip in ips_to_check:
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {'x-apikey': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Basic IP information
        ip_address = data["data"]["id"]
        reputation = data["data"]["attributes"]["reputation"]
        last_analysis_stats = data["data"]["attributes"]["last_analysis_stats"]
        
        print(f'IP Address: {ip_address}')
        print(f'Reputation: {reputation}')

        # Last analysis statistics
        print(f'Malicious: {last_analysis_stats["malicious"]}')
        print(f'Suspicious: {last_analysis_stats["suspicious"]}')
        print(f'Harmless: {last_analysis_stats["harmless"]}')
        print(f'Undetected: {last_analysis_stats["undetected"]}')

        # Whois information
        whois = data["data"]["attributes"]["whois"]
        if whois:
            try:
                whois_dict = json.loads(whois)
                print("Whois Information:")
                for key, value in whois_dict.items():
                    print(f'{key}: {value}')
            except json.JSONDecodeError:
                print(f"Error parsing Whois information: {whois}")
        else:
            print("No Whois Information available for this IP")

        # Scan results
        scan_results = data["data"]["attributes"]["last_analysis_results"]
        print("\nScan Results:")
        for engine, result in scan_results.items():
            print(f'Engine: {engine}')
            print(f'Result: {result["result"]}')
            print(f'Category: {result["category"]}\n')

        print("-" * 40)
    else:
        print(f'IP: {ip}, Error: {response.status_code}')
