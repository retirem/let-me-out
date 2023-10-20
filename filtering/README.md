# Filtering a blocklist containing IPs and subnets based on specified networks.

Make sure that the following python packages are properly installed and updated.

ipaddress, argparse, sys


## Usage:

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
