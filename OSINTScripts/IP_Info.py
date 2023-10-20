class IP_Info:
    def __init__(self, read_ip: str) -> None:
        self.ip_address = read_ip
        self.ip: str = ''
        self.network: str = ''
        self.virustotal: dict = {}
        self.ipqualityscore: dict = {}
