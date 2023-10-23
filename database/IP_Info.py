class IP_Info:
    def __init__(self, read_ip: str) -> None:
        self.ip_address = read_ip
        self.ip: str = self.ip_address.split('/')[0]
        self.network: str = ''
        self.virustotal: dict = {
            'reputation': 0,
            'harmless_count': 0,
            'suspicious_count': 0,
            'malicious_count': 0,
            'undetected_count': 0,
        }
        self.ipqualityscore: dict = {
            'is_proxy': False,
            'is_vpn': False,
            'is_tor': False,
            'is_bot': False,
            'risk_score': 0,
            'geolocation': {
                'city': '',
                'region': '',
                'country': '',
            },
        }
