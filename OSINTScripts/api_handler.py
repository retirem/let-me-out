import sys, logging

class APIHandler:
    def __init__(self, virustotal_keys: list[str], abuseIPDB_keys: list[str]) -> None:
        self.virustotal_keys = virustotal_keys
        self.virustotal_current_key_index = 0
        self.virustotal_usage_count = 0
        self.virustotal_daily_limit = 500
        self.virustotal_minute_limit = 4
        self.abuseIPDB_keys = abuseIPDB_keys
        self.abuseipDB_current_key_index = 0
        self.abuseIPDB_usage_count = 0
        self.abuseIPDB_dayli_limit = 2000 # TODO this number is imaginary, we need to rethink this with Shreyas

    def get_virustotal_key(self) -> str:
        self.virustotal_usage_count += 1
        if self.virustotal_usage_count > self.virustotal_daily_limit:
            self.virustotal_current_key_index += 1

        if self.virustotal_current_key_index == len(self.virustotal_keys):
            logging.error('There are no more VirusTotal keys to use.')
            sys.exit(1)

        return self.virustotal_keys[self.virustotal_current_key_index]
    
    def get_virustotal_key_index(self, index: int) -> str:
        return self.virustotal_keys[index]
    
    def get_virustotal_key_count(self) -> int:
        return len(self.virustotal_keys)

    def get_abuseIPDB_key(self) -> str:
        self.abuseIPDB_usage_count += 1
        if self.abuseIPDB_usage_count > self.abuseIPDB_dayli_limit:
            self.abuseipDB_current_key_index += 1

        if self.abuseipDB_current_key_index == len(self.abuseIPDB_keys):
            logging.error('There are no more IPQualityScore keys to use.')
            sys.exit(1)

        return self.abuseIPDB_keys[self.abuseipDB_current_key_index]
