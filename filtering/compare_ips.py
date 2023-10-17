import ipaddress
import argparse
import sys


#TODOs:
#   1. write the output to a file (.txt)
#   2. logging ???


def argument_parse():
    try:
        # Specify the arguments parsed from the command line
        parser = argparse.ArgumentParser(description='Filtering IPs and networks from File1 based on the networks specified in File2.')
        parser.add_argument('--blocklist', type=str, required=True, help='The .txt file containing the blocklisted IPs.')
        parser.add_argument('--networks', type=str, required=True, help="The .txt file containing the chosen country's subnets")
        args = parser.parse_args()
        blocklist = args.blocklist
        networks = args.networks
        print("[+] Opening the specified files ...")
        return blocklist, networks
    except Exception as ex:
        print(ex)
        sys.exit(1)

def blocked_ips(filename: str):
    try:
        # Read the blocklist .txt file and load it's content into a list.
        with open(filename, "r") as file1:
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
            print("[-] The IP addresses in " + filename +" are in a bad format.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Unable to open the "+ filename + " file.")
        print(ex)
        sys.exit(1)



def danish_subnets(filename: str):
    try:
        # Read the networks .txt file.
        with open(filename, "r") as file2:
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
            print("[-] The networks in " + filename +" are in a bad format.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Unable to open the "+ filename + " file.")
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

        ## Writing the results to the terminal.
        #if matches:
        #    for match in matches:
        #        print(f"Danish: {match[0]}, network: {match[1]}")
        else:
            print("[+] No matching IP addresses within networks found.")
    except Exception as ex:
        print("[-] For some reason filtering is not possible!")
        print(ex)    
        sys.exit(1)


if __name__ == "__main__":

    arguments = argument_parse()

    print("[+] Starting the script ... ")

    blocked = blocked_ips(arguments[0])
    subnets = danish_subnets(arguments[1])
    filtering(ip_addresses=blocked[0], subnets=subnets, networks=blocked[1])