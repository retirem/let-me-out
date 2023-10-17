import os, sys

from configparser import ConfigParser
from argparse import ArgumentParser

# Run this script to restore database from a specific backup file

def read_db_config(config_path: str) -> (str, str):
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(config_path)

    if config_parser['DB.Credentials']['User'] and config_parser['DB.Credentials']['Password']:
        return (config_parser['DB.Credentials']['User'], config_parser['DB.Credentials']['Password'])
    else:
        print('Missing configuration.')
        print('Exiting now...')
        sys.exit(1)

def input_backup_path() -> (str, str):
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-b', '--backup', help='Path to backup file', required=True)
    parser.add_argument('-c', '--config', help='Path to DB config gile', required=False, default='db.conf')

    args = parser.parse_args()
    backup_path: str = args.backup
    config_path: str = args.config

    if os.path.exists(backup_path) and os.path.isfile(backup_path) and backup_path.endswith('.tar'):
        if os.path.exists(config_path) and os.path.isfile(config_path):
            return (backup_path, config_path)
    else:
        print('Error during checking backup path.')
        print('Exiting now...')
        sys.exit(1)


if __name__ == "__main__":
    (backup_path, config_path) = input_backup_path()
    (username, password) = read_db_config(config_path=config_path)

# TODO read database config

# TODO check DB availability/connect to DB

# TODO run backup on DB
