import sys, logging

class APIHandler:
    def __init__(self, virustotal_keys: list[str], ipqualityscore_keys: list[str]) -> None:
        self.virustotal_keys = virustotal_keys
        self.virustotal_current_key_index = 0
        self.virustotal_usage_count = 0
        self.virustotal_daily_limit = 500
        self.virustotal_minute_limit = 4
        self.ipqualityscore_keys = ipqualityscore_keys
        self.ipqualityscore_current_key_index = 0
        self.ipqualityscore_usage_count = 0
        self.ipqualityscore_daily_limit = 2000 # TODO this number is imaginary, we need to rethink this with Shreyas

    def get_virustotal_key(self) -> str:
        self.virustotal_usage_count += 1
        if self.virustotal_usage_count > self.virustotal_daily_limit:
            self.virustotal_current_key_index += 1

        if self.virustotal_current_key_index == len(self.virustotal_keys):
            logging.error('There are no more VirusTotal keys to use.')
            sys.exit(1)

        return self.virustotal_keys[self.virustotal_current_key_index]

    def get_ipqualityscore_key(self) -> str:
        self.ipqualityscore_usage_count += 1
        if self.ipqualityscore_usage_count > self.ipqualityscore_daily_limit:
            self.ipqualityscore_current_key_index += 1

        if self.ipqualityscore_current_key_index == len(self.ipqualityscore_keys):
            logging.error('There are no more IPQualityScore keys to use.')
            sys.exit(1)

        return self.ipqualityscore_keys[self.ipqualityscore_current_key_index]
