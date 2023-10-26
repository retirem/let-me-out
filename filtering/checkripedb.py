import requests, sys, os
from configparser import ConfigParser

# TODO:
#   - rename the variables
#   - specify JSON response
#   - set logging

def get_conf() -> str:
    conf_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../script.conf')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(conf_path)
    return config_parser.get('CONFIGS', 'workdir_todays')


def check_ripe_database():
    input_filename: str = os.path.join(working_directory, 'blocked_ips_networks.txt')
    try:
        with open(input_filename, "r") as file:
            ips = file.read().splitlines()
        int_not_danish_byRIPEdb = 0
        int_danish_byRIPEdb = 0
        not_danish = set()

        try:
            for ip in ips:
                url = f"http://rest.db.ripe.net/search?flags=no-personal&query-string={ip}"
                respond = requests.get(url)
                DK = '<attribute name="country" value="DK"/>'
                dk = '<attribute name="country" value="dk"/>'
                Dk = '<attribute name="country" value="Dk"/>'
                dK = '<attribute name="country" value="dK"/>'
                if (DK or dk or Dk or dK) in respond.text:
                    int_danish_byRIPEdb += 1
                else:
                    int_not_danish_byRIPEdb += 1
                    not_danish.add(ip)
            with open(os.path.join(working_directory, 'ripeDB_check.txt'), "w") as output:
                output.write(str(int_not_danish_byRIPEdb) + "\n")
        except Exception as ex:
            print("[-] Failed to send requests to the RIPE DB.")
            print(ex)
            sys.exit(1)
    except Exception as ex:
        print("[-] Failed to open the blocked_ips_networks.txt file.")
        print(ex)
        sys.exit(1)



if __name__ == "__main__":
    global working_directory
    working_directory = get_conf()

    check_ripe_database()
    

