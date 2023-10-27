import requests, sys, os
from configparser import ConfigParser

# TODO:
#   - set logging

def get_conf() -> str:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return config_parser.get('CONFIGS', 'workdir_todays')

def NETcheck_ripe_database():
    input_net_filename: str = os.path.join(working_directory, 'blocked_networks.txt')

    try:
        with open(input_net_filename, "r") as file:
            netw = file.read().splitlines()
        net_not_danish_byRIPEdb = 0
        net_danish_byRIPEdb = 0
        net_not_danish = set()
        try:
            for nets in netw:
                url = f"http://rest.db.ripe.net/search?flags=no-personal&query-string={nets}"
                respond = requests.get(url)
            DK = '<attribute name="country" value="DK"/>'
            dk = '<attribute name="country" value="dk"/>'
            Dk = '<attribute name="country" value="Dk"/>'
            dK = '<attribute name="country" value="dK"/>'
            if (DK or dk or Dk or dK) in respond.text:
                net_danish_byRIPEdb += 1
            else:
                net_not_danish_byRIPEdb += 1
                net_not_danish.add(ip)
            with open(os.path.join(working_directory, 'NET_ripeDB_check.txt'), "w") as output:
                output.write(str(net_not_danish_byRIPEdb) + "\n")
        except Exception as ex:
            print("[-] Failed to send requests (containing blocked networks) to the RIPE DB.")
            print(ex)
            sys.exit(1)
    
    except Exception as ex:
        print("[-] Failed to open the blocked_ips_networks.txt file during the networks check.")
        print(ex)
        sys.exit(1)


def IPcheck_ripe_database():
    input_ip_filename: str = os.path.join(working_directory, 'unique_blocked_ips.txt')
    
    try:
        with open(input_ip_filename, "r") as file:
            ips = file.read().splitlines()
    
        ip_not_danish_byRIPEdb = 0
        ip_danish_byRIPEdb = 0
        ip_not_danish = set()

        # Blocked ip check
        try:
            for ip in ips:
                url = f"http://rest.db.ripe.net/search?flags=no-personal&query-string={ip}"
                respond = requests.get(url)
                DK = '<attribute name="country" value="DK"/>'
                dk = '<attribute name="country" value="dk"/>'
                Dk = '<attribute name="country" value="Dk"/>'
                dK = '<attribute name="country" value="dK"/>'
                if (DK or dk or Dk or dK) in respond.text:
                    ip_danish_byRIPEdb += 1
                else:
                    ip_not_danish_byRIPEdb += 1
                    ip_not_danish.add(ip)
            with open(os.path.join(working_directory, 'IP_ripeDB_check.txt'), "w") as output:
                output.write(str(ip_not_danish_byRIPEdb) + "\n")
        except Exception as ex:
            print("[-] Failed to send requests (containing blocked IPs) to the RIPE DB.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Failed to open the blocked_ips_networks.txt file during the IPs check.")
        print(ex)
        sys.exit(1)



if __name__ == "__main__":
    global working_directory
    working_directory = get_conf()

    IPcheck_ripe_database()
    NETcheck_ripe_database()
    

