import logging, sys, os, pwd

from subprocess import PIPE, run, CompletedProcess
from shutil import which
from argparse import ArgumentParser
from datetime import datetime
from configparser import ConfigParser


def parse_arguments() -> str:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-w', '--workdir', type=str, help='Working directory path which all the scripts are going to use.', required=True)
    args = parser.parse_args()
    return str(args.workdir)

def initialize_working_directory(directory: str) -> str:
    print('Using the provided working directory: ' + directory)
    if not os.path.exists(directory):
        try:
            print('Trying to create directory at: ' + directory)
            os.mkdir(directory)
            print('Directory successfully created.')
        except Exception as ex:
            print('An error happened during creation of the directory: ' + str(ex.args))
            print('Exiting now...')
            sys.exit(1)
    print('Creating working directory for today...')
    work_dir: str = os.path.join(directory, str(datetime.now().date()))
    try:
        os.mkdir(work_dir)
    except Exception as ex:
        print('An error happened during creation of today\'s directory: ' + str(ex.args))
        print('Exiting now...')
        sys.exit(1)

    print('Setting working directory in script.conf file.')
    config_parser: ConfigParser = ConfigParser()
    config_parser.read('../script.conf')
    config_parser.set('CONFIGS', 'WORKDIR', work_dir)
    with open('../script.conf', 'w') as config_file:
        config_parser.write(config_file)
    print('Working directory set in script.conf file.')

    return work_dir

def initialize_config_file(config_path: str) -> None:
    logging.info('Creating config file in working directory.')
    # This format is required for update-ipsets command
    with open(config_path, 'w') as config_file:
        config_file.write('BASE_DIR=' + os.path.join(working_directory, 'ipsets'))
    logging.info('Config file created.')

def configure_logging() -> None:
    log_path: str = os.path.join(working_directory, 'fetch_ips.log')
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

def aggregate_ipsets() -> None:
    output_IPs: set[str] = set()
    ipsets_directory: str = os.path.join(working_directory, 'ipsets')

    try:
        for file_name in os.listdir(ipsets_directory):
            if file_name.endswith('.ipset') or file_name.endswith('.netset'):
                with open(os.path.join(ipsets_directory, file_name), 'r') as opened_file:
                    IPs: list[str] = opened_file.readlines()
                    for IP in IPs:
                        # There are comment lines starting with # in the files which are useless
                        if not IP.startswith('#'):
                            output_IPs.add(IP)
    except Exception as ex:
        logging.error('Error during the aggregation of IP sets: ' + str(ex.args))
        print('Exiting now...')
        sys.exit(1)
    with open(os.path.join(working_directory, 'aggregated_iplists.txt'), 'w') as output:
        output.writelines(sorted(output_IPs))


if __name__ == "__main__":
    print('Starting IP fetching script...')

    workdir = parse_arguments()
    todays_workdir: str = initialize_working_directory(directory=workdir)

    # Set it here to satisfy mypy, if the execution reaches this point the workdir is initialized
    global working_directory
    working_directory = todays_workdir

    configure_logging()

    config_path: str = os.path.join(working_directory, 'update-ipsets.conf')
    initialize_config_file(config_path=config_path)

    check_command_availability('update-ipsets')

    update_ipsets(config_path=config_path)
    aggregate_ipsets()

    print('Exiting ip fetching script... Bye.')
