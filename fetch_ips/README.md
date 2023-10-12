# Fetching blocked IPs and maintin a list of blocked Danish IP addresses

## Install `update-ipsets` package from FireHol

Install the `update-ipsets` from the FireHol project: https://github.com/firehol/blocklist-ipsets 

Follow the installation instructions provided here: https://github.com/firehol/blocklist-ipsets/wiki/Installing-update-ipsets

This is a copy on the date 12/10/2023:
```sh
sudo apt-get install autoconf autogen automake curl gcc git ipset kmod make pkg-config procps traceroute zlib1g-dev
```

```sh
# cd somewhere
cd /tmp

# download iprange and firehol from github
git clone https://github.com/firehol/iprange.git iprange.git
git clone https://github.com/firehol/firehol.git firehol.git

# install iprange
cd iprange.git

./autogen.sh
# make sure it completed successfully

./configure --prefix=/usr CFLAGS="-march=native -O3" --disable-man
# make sure it completed successfully

make
# make sure it completed successfully

sudo make install
# make sure it completed successfully

# install firehol
cd ../firehol.git

./autogen.sh
# make sure it completed successfully

./configure --prefix=/usr --sysconfdir=/etc --disable-man --disable-doc
# make sure it completed successfully

make
# make sure it completed successfully

sudo make install
# make sure it completed successfully

# Create the default RUN_PARENT_DIR='/usr/var/run' who is set in '/etc/firehol/update-ipsets.conf'
mkdir -p /usr/var/run
```

## Running `update-ips` Python script

Created a Python script which using the `update-ipsets` command and extracts the blocked IP addresses into one `.txt` file.

Prerequisities:
- `update-ipsets` is installed and in `$PATH`
- Python3 is installed (and possibly in `$PATH`)

You can run the script by:
```sh
python update_ips.py
```

Output:
- `aggregated_iplists.txt` with all the IPs from the blocklists, uniquely and sorted
- `fetch_ips.log` log file which contains all the actions taken by the script

## Extract Danish IPs from the aggregated blocklist

## Save IPs in database

