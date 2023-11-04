class IP_Info:
    def __init__(self, read_ip: str) -> None:
        self.ip_address = read_ip
        self.ip: str = self.ip_address.split('/')[0]
        self.network: str = ''
        self.virustotal: dict = {}
        self.abuseipdb_data: dict = {}
