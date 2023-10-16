import logging, sys, os, pwd

from subprocess import PIPE, run, CompletedProcess
from shutil import which
from datetime import datetime


def initialize_working_directory(directory: str) -> None:
    try:
        print('Trying to create working directory at: ' + directory)
        os.mkdir(directory)
        print('Working directory successfully created.')
    except Exception as ex:
        print('An error happened during creation of the working directory: ' + str(ex.args))
        print('Exiting now...')
        sys.exit(1)

def initialize_config_file(working_directory: str, config_path: str) -> None:
    logging.info('Creating config file in working directory.')
    with open(config_path, 'w') as config_file:
        config_file.write('BASE_DIR=' + working_directory + '/ipsets\n')
    logging.info('Config file created.')

def configure_logging(working_directory: str) -> None:
    log_path: str = working_directory + '/fetch_ips.log'
    handlers: list[logging.Handler] = [logging.FileHandler(filename=log_path), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def check_command_availability(command: str) -> None:
    logging.info('Checking for update-ipsets command availability...')
    if which(command) is None:
        logging.error('update-ipset command is not available in the $PATH, please install it from: https://github.com/firehol/blocklist-ipsets/wiki/Installing-update-ipsets.')
        sys.exit(1)
    logging.info('Update-ipsets command is available.')

def update_ipsets(config_path: str) -> None:
    update_ipsets_parameters: list[str] = ['--enable-all', '--config', config_path]
    logging.info('Executing update-ipsets with the following parameters: ' + ', '.join(update_ipsets_parameters))
    print('This can take a while...')

    result: CompletedProcess = run(['update-ipsets', *update_ipsets_parameters], stderr=PIPE, universal_newlines=True)
    if result.returncode != 0:
        logging.error('An error happened during executing update-ipsets command: ' + str(result.stderr))
        print('Exiting now...')
        sys.exit(1)

    logging.info('Finished update-ipsets command. Updated ipsets can be found in the ~/ipsets folder, if the config file has not been modified.')

def aggregate_ipsets(working_directory: str) -> None:
    output_IPs: set(str) = set()
    ipsets_directory: str = working_directory + '/ipsets'

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

    with open(working_directory + '/aggregated_iplists.txt', 'w') as output:
        output.writelines(sorted(output_IPs))


if __name__ == "__main__":
    print('Starting IP fetching script...')

    working_directory: str = '/home/' + pwd.getpwuid(os.getuid()).pw_name + '/let-me-out'
    initialize_working_directory(directory=working_directory)

    configure_logging(working_directory=working_directory)

    config_path: str = working_directory + '/update-ipsets.conf'
    initialize_config_file(working_directory=working_directory, config_path=config_path)

    check_command_availability('update-ipsets')

    update_ipsets(config_path=config_path)
    aggregate_ipsets(working_directory=working_directory)

    print('Exiting ip fetching script... Bye.')
