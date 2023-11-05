import sys, os

from datetime import date, timedelta
from ipaddress import IPv4Address, IPv4Network
from configparser import ConfigParser


def get_conf() -> tuple[str, str]:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return (config_parser.get('CONFIGS', 'workdir'),
            config_parser.get('CONFIGS', 'workdir_todays'))

def blocked_ips():
    blocklist_path: str = os.path.join(working_directory, 'aggregated_iplists.txt')
    try:
        # Read the blocklist .txt file and load it's content into a list.
        with open(blocklist_path, "r") as file1:
            ips = file1.read().splitlines()
        ip_addresses = []
        blocked_networks = []
        try:
            for ip in ips:
                ip = ip.strip()
                try:
                    # Creating the blocked IPs list.
                    ip = IPv4Address(ip)
                    ip_addresses.append(ip)
                except:
                    try:
                        # Creating the blocked networks list.
                        ip = IPv4Network(ip)
                        blocked_networks.append(ip)
                    except Exception as ex:
                        print("[-] Invalid element in the blocked list!")
                        print(ex)
                        sys.exit(1)
            print("[+] Blocklist loaded!")
            return ip_addresses, blocked_networks
        except Exception as ex:
            print("[-] The IP addresses in " + blocklist_path +" are in a bad format.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Unable to open the "+ blocklist_path + " file.")
        print(ex)
        sys.exit(1)

def danish_subnets():
    network_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'danish_networks.txt')

    try:
        # Read the networks .txt file.
        with open(network_path, "r") as file2:
            subs = file2.read().splitlines()
        subnets = []
        try:
            # Creating the networks list in the variable: subnets.
            for sub in subs:
                sub = sub.strip()
                subnet = IPv4Network(sub)
                subnets.append(subnet)
            print("[+] Networks loaded!")
            return subnets
        except Exception as ex:
            print("[-] The networks in " + network_path +" are in a bad format.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Unable to open the "+ network_path + " file.")
        print(ex)
        sys.exit(1)

def filtering(ip_addresses: list, subnets: list, networks: list) -> set[tuple[IPv4Address|IPv4Network, IPv4Network]]:
    try:
        print("[+] Filtering started ...\n[!] The output is two files: blocked_unique_ips.txt and blocked_networks.txt\n\n[!]This will take a while.\n\n")
        ip_matches = set()
        network_matches = set()

        # Checks wether the blocked IPs are hosts in at least one network.
        for ip in ip_addresses:
            for subnet in subnets:
                if ip in subnet:
                    ip_matches.add((ip, subnet))
        # Check wether the blocked networks are subnets at least one network.
        for net in networks:
            for subnet in subnets:
                if net.subnet_of(subnet):
                    network_matches.add((net, subnet))

        # Write the Danish blocked IPs and the corresponding Danish networks to a .txt file.
        if ip_matches:
            with open(os.path.join(working_directory, 'unique_blocked_ips.txt'), "w") as output:
                index_ip = 1
                for element in ip_matches:
                    if index_ip == len(ip_matches):
                        output.write(str(element[0]))
                    else:
                        output.write(str(element[0]) + "\n")
        else:
            print("[-/+] No matching blocked IP addresses within the Danish networks found.")
        
        # Write the Danish blocked subnetworks and the corresponding Danish networks to a .txt file.
        if network_matches:
            with open(os.path.join(working_directory, 'blocked_networks.txt'), "w") as output:
                index_net = 1
                for element in network_matches: 
                    if index_net == len(network_matches):
                        output.write(str(element[0]))
                    else:
                        output.write(str(element[0]) + "\n")

        else:
            print("[-/+] No matching blocked networks within the Danish networks found.")
    except Exception as ex:
        print("[-] For some reason filtering is NOT possible!")
        print(ex)    
        sys.exit(1)


if __name__ == "__main__":
    global root_working_directory, working_directory
    (root_working_directory, working_directory) = get_conf()

    print("[+] Starting the script ... ")

    blocked = blocked_ips()
    subnets = danish_subnets()
    filtered: set[tuple[IPv4Address|IPv4Network, IPv4Network]] = filtering(ip_addresses=blocked[0], subnets=subnets, networks=blocked[1])
