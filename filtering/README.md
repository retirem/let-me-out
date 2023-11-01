# Filtering a blocklist containing IPs and subnets based on specified networks.

Make sure that the following python packages are properly installed and updated.

ipaddress, argparse, sys

# Filter Danish IPs and networks
## compare_ips.py USAGE:

```sh
usage: compare_ips.py [-h] --blocklist BLOCKLIST --networks NETWORKS

Filtering IPs and networks from File1 based on the networks specified in File2.

optional arguments:
  -h, --help            show this help message and exit
  --blocklist BLOCKLIST
                        The .txt file containing the blocklisted IPs.
  --networks NETWORKS   The .txt file containing the chosen country's networks.
```
### Example
```sh
python compare_ips.py --blocklist file1.txt --networks file2.txt
```

## Troubleshooting
(Date of creation: 17 October 2023)

Nothing yet.

# Check the country code on the RIPE DB (RIPE NCC).
This script takes networks and IPs from two different .txt files, and checks the country based on the RIPE NCC's database, wether they are Danish or not.

## checkripedb.py USAGE
Using the .txt files as INPUTS from the working directory (specified in the /script.conf file).
    - from compare_ips.py script blocked_networks.txt
    - from compare_ips.py script unique_blocked_ips.txt

The OUTPUTS are the next .txt files:
    - IP_ripeDB_check.txt
    - NET_ripeDB_check.txt

### Example
```sh
python checkripedb.py
```

## Troubleshooting
(Date of creation: 1 November 2023)

Nothing yet.
