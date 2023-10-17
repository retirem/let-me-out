# Create PostgreSql database and import backup

## Run PostgreSql

Complete these steps to run `PostgreSql` on your machine.

### Install PostgreSql

The following steps are required to install `PostgreSql` on a Debian based Linux machine, taken from [www.postgresql.org](https://www.postgresql.org/download/linux/debian/) on 17/10/2023:
```sh
# Create the file repository configuration:
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql
``` 

For other OS systems please see the othe descriptions on the website.

### Run PostgreSql

```sh
sudo systemctl enable postgresql

sudo systemctl start postgresql
```

To see status of `PostgreSql` service:
```sh
sudo systemctl status postgresql
```

## Import backup

## Create backup

## Credentials