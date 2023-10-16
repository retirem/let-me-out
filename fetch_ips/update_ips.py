import logging, sys, os, pwd

from subprocess import PIPE, run, CompletedProcess
from shutil import which
from datetime import datetime


def tool_not_exists(name: str) -> bool:
    return which(name) is None

def logging_time() -> str:
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def initialize_working_directory(directory: str, config_path: str) -> None:
    try:
        logging.info('Trying to create working directory.')
        os.mkdir(directory)
    except Exception as ex:
        logging.error('An error happened during creation of the working directory: ' + str(ex.args))
        print('Exiting now...')
        sys.exit(1)
    else:
        logging.info('Working directory successfully created and can be found here: ' + directory)
        logging.info('Creating config file in working directory.')
        with open(config_path, 'w') as config_file:
            config_file.write('BASE_DIR=' + directory + '/ipsets\n')
        logging.info('Config file created.')

def configure_logging() -> None:
    handlers: list[logging.Handler] = [logging.FileHandler(filename='fetch_ips.log'), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

def update_ipsets(config_path: str) -> None:
    update_ipsets_parameters: list[str] = ['--enable-all', '-f', config_path]
    logging.info('Executing update-ipsets with the following parameters: ' + ', '.join(update_ipsets_parameters))
    print('This can take a while...')

    result: CompletedProcess = run(['update-ipsets', ' '.join(update_ipsets_parameters)], stderr=PIPE, universal_newlines=True)
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
    configure_logging()

    working_directory: str = '/home/' + pwd.getpwuid(os.getuid()).pw_name + '/let-me-out'
    config_path: str = working_directory + '/update-ipsets.conf'
    initialize_working_directory(directory=working_directory, config_path=config_path)

    logging.info('Checking for update-ipsets command availability...')
    if tool_not_exists('update-ipsets'):
        logging.error(logging_time() + " update-ipset command is not available in the $PATH, please install it from: https://github.com/firehol/blocklist-ipsets/wiki/Installing-update-ipsets.")
        sys.exit(1)
    logging.info('Update-ipsets command is available.')

    update_ipsets(config_path=config_path)
    aggregate_ipsets(working_directory=working_directory)

    print('Exiting ip fetching script... Bye.')
