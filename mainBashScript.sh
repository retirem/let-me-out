#!/bin/bash

set -e

# Fetching all the blocked IPs from Firehol
python /home/letmeout/git/let-me-out/fetch_ips/update_ips.py

# Run compare_ips.py to filter the fetched IPs and save to the output file
python /home/letmeout/git/let-me-out/filtering/compare_ips.py

# Run analyzing.py to see which IP adresses are malicious and their quality score
python /home/letmeout/git/let-me-out/OSINTScripts/analyzing.py

#Run the ripecheck script
#python /home/letmeout/git/let-me-out/filtering/checkripedb.py

# Upload data to the database
python /home/letmeout/git/let-me-out/database/txt_to_db.py
