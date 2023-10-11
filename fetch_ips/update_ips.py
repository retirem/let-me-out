import logging
import sys
import subprocess

from shutil import which
from datetime import datetime

def tool_not_exists(name: str) -> bool:
    return which(name) is None

def logging_time() -> str:
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def configure_logging() -> None:
    handlers = [logging.FileHandler(filename='fetch_ips.log'), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

if __name__ == "__main__":
    configure_logging()
    print('Starting ip fetching script...')

    logging.info('Checking for update-ipsets command availability...')
    if tool_not_exists('update-ipsets'):
        logging.error(logging_time() + " update-ipset command is not available in the $PATH, please install it from: https://github.com/firehol/blocklist-ipsets/wiki/Installing-update-ipsets.")
        sys.exit(1)
    logging.info('Update-ipsets command is available.')

    update_ipsets_parameters: list[str] = ['--enable all']
    
    logging.info('Executing update-ipsets with the following parameters:' + ', '.join(update_ipsets_parameters))
    print('This can take a while...')
    subprocess.run(['update-ipsets', *update_ipsets_parameters])
    logging.info('Finished update-ipsets command. Updated ipsets can be found in the ~/ipsets folder, if the config file has not been modified.')

    print('Exiting ip fetching script... Bye.')
