import ipaddress, sys, os, shutil

from configparser import ConfigParser


def get_conf() -> str:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return config_parser.get('CONFIGS', 'workdir_todays')

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
                    ip = ipaddress.IPv4Address(ip)
                    ip_addresses.append(ip)
                except:
                    try:
                        # Creating the blocked networks list.
                        ip = ipaddress.IPv4Network(ip)
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
    nework_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'danish_networks.txt')

    try:
        # Read the networks .txt file.
        with open(nework_path, "r") as file2:
            subs = file2.read().splitlines()
        subnets = []
        try:
            # Creating the networks list in the variable: subnets.
            for sub in subs:
                sub = sub.strip()
                subnet = ipaddress.IPv4Network(sub)
                subnets.append(subnet)
            print("[+] Networks loaded!")
            return subnets
        except Exception as ex:
            print("[-] The networks in " + nework_path +" are in a bad format.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Unable to open the "+ nework_path + " file.")
        print(ex)
        sys.exit(1)

def filtering(ip_addresses: list, subnets: list, networks: list):
    try:
        print("[+] Filtering started ...\n\n This will take a while.\n\n")
        matches = set()
        # Checks wether the blocked IPs are hosts in at least one network.
        for ip in ip_addresses:
            for subnet in subnets:
                if ip in subnet:
                    matches.add((ip, subnet))
        # Check wether the blocked networks are subnets at least one network.
        for net in networks:
            for subnet in subnets:
                if net.subnet_of(subnet):
                    matches.add((net, subnet))

        if matches:

            with open(os.path.join(working_directory, 'blocked_ips_networks.txt'), "w") as output:
                for element in matches:
                    output.write(str(element[0]) + "\n")

            ## Writing the results to the terminal.
            #for match in matches:
            #    print(f"Danish: {match[0]}, network: {match[1]}")

            ## Uncomment the next 3 lines to make a summarised list.
            #with open("sum.txt", "w") as output:
            #    for element in matches:
            #        output.write(str(element[0])+ " , " +str(element[1]) + "\n")

            ## Uncomment the next 3 lines to make a list of just the containing networks.
            #with open("containing_network.txt", "w") as output:
            #    for element in matches:
            #        output.write(str(element[1]) + "\n")

        else:
            print("[+] No matching IP addresses within networks found.")
    except Exception as ex:
        print("[-] For some reason filtering is not possible!")
        print(ex)    
        sys.exit(1)


if __name__ == "__main__":
    global working_directory
    working_directory = get_conf()

    print("[+] Starting the script ... ")

    blocked = blocked_ips()
    subnets = danish_subnets()
    filtering(ip_addresses=blocked[0], subnets=subnets, networks=blocked[1])
