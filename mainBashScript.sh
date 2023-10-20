#!/bin/bash

# Fetching all the blocked IPs from Firehol
python3 fetch_ips/update_ips.py 

echo "Fetching done"

# Run compare_ips.py to filter the fetched IPs and save to the output file
python3 filtering/compare_ips.py --blocklist "../aggregated_iplists.txt" --networks "../dk-aggregated.zone.txt" 

echo "Filtering done"

# Run analyzing.py to see which IP adresses are malicious and their quality score
python3 OSINTScripts/analyzing.py -w "../"

echo "Maliciousness and quality tested. Results are in:"