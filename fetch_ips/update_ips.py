import logging, sys, os, pwd

from subprocess import PIPE, run, CompletedProcess
from shutil import which
from datetime import datetime


def tool_not_exists(name: str) -> bool:
    return which(name) is None

def logging_time() -> str:
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def configure_logging() -> None:
    handlers: list[logging.Handler] = [logging.FileHandler(filename='fetch_ips.log'), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def update_ipsets() -> None:
    # TODO Maybe BASE_DIR should be made fixed, by the script
    update_ipsets_parameters: list[str] = ['--enable-all']
    logging.info('Executing update-ipsets with the following parameters: ' + ', '.join(update_ipsets_parameters))
    print('This can take a while...')

    result: CompletedProcess = run(['update-ipsets', *update_ipsets_parameters], stderr=PIPE, universal_newlines=True)
    if result.returncode != 0:
        logging.error('An error happened during executing update-ipsets command: ' + str(result.stderr))
        print('Exiting now...')
        sys.exit(1)

    logging.info('Finished update-ipsets command. Updated ipsets can be found in the ~/ipsets folder, if the config file has not been modified.')

def aggregate_ipsets() -> None:
    # By default of running update-ipsets without root user, the ip sets are located in ~/ipsets folder with .ipset, .netset extensions
    output_IPs: set(str) = set()
    ipsets_directory: str = '/home/' + pwd.getpwuid(os.getuid()).pw_name + '/ipsets'

    try:
        for file_name in os.listdir(ipsets_directory):
            if file_name.endswith('.ipset') or file_name.endswith('.netset'):
                with open(ipsets_directory + '/' + file_name, 'r') as opened_file:
                    IPs: list[str] = opened_file.readlines()
                    for IP in IPs:
                        # There are comment lines starting with # in the files which are useless
                        if not IP.startswith('#'):
                            output_IPs.add(IP)
    except Exception as ex:
        logging.error('Error during the aggregation of IP sets: ' + str(ex.args))
        print('Exiting now...')
        sys.exit(1)

    with open('aggregated_iplists.txt', 'w') as output:
        output.writelines(sorted(output_IPs))


if __name__ == "__main__":
    configure_logging()
    print('Starting IP fetching script...')

    logging.info('Checking for update-ipsets command availability...')
    if tool_not_exists('update-ipsets'):
        logging.error(logging_time() + " update-ipset command is not available in the $PATH, please install it from: https://github.com/firehol/blocklist-ipsets/wiki/Installing-update-ipsets.")
        sys.exit(1)
    logging.info('Update-ipsets command is available.')

    update_ipsets()
    aggregate_ipsets()

    print('Exiting ip fetching script... Bye.')
