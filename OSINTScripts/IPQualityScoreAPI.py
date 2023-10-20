
for ip in ips_to_check:
    url = f'https://ipqualityscore.com/api/json/ip/{api_key}/{ip}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Basic IP information
        ip_address = data.get("ip_address")
        is_proxy = data.get("proxy")
        is_vpn = data.get("vpn")
        is_tor = data.get("tor")
        is_bot = data.get("is_bot")
        
        print(f'IP Address: {ip_address}')
        print(f'Is Proxy: {is_proxy}')
        print(f'Is VPN: {is_vpn}')
        print(f'Is Tor Exit Node: {is_tor}')
        print(f'Is Bot: {is_bot}')

        # Risk Score
        risk_score = data.get("risk_score")
        print(f'Risk Score: {risk_score}')

        # Location Information
        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        print(f'City: {city}')
        print(f'Region: {region}')
        print(f'Country: {country}')

        print("-" * 40)
    else:
        print(f'IP: {ip}, Error: {response.status_code}')


# retrieves information about each IP, including whether it's a proxy, VPN, Tor exit node, or a bot, the risk score associated with the IP, and location information

if __name__ == '__main__':
    (ip_file_path, workdir): str = parse_arguments()
    configure_logging(working_directory=workdir)
    ips: list[str] = read_ips(filepath=ip_file_path)


