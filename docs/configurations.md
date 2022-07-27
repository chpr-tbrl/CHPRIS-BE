# Configurations

## Table of contents

1. [Requirements](#requirements)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Setup](#setup)
5. [How to use](#how-to-use)

## Requirements

- [MySQL](https://www.mysql.com/) (version >= 8.0.28) ([MariaDB](https://mariadb.org/))
- [Python](https://www.python.org/) (version >= [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Dependencies

On Ubuntu **libmysqlclient-dev** is required

```
sudo apt install python3-dev libmysqlclient-dev
sudo apt-get install libapache2-mod-wsgi-py3 
```

If using apache2 wsgi on Ubuntu

```
sudo apt-get install libapache2-mod-wsgi-py3 
```

## Installation

Create a Virtual Environments **(venv)**

```
python3 -m venv venv
```

Move into Virtual Environments workspace

```
. venv/bin/activate
```

Install all python packages

```
python3 -m pip install -r requirements.txt
```

## Setup

All configuration files are found in the **[configs](../configs)** directory.

### configuration file

To set up Database and API, copy the template files "example.default.ini" and rename to "default.ini"

```
cp configs/example.default.ini configs/default.ini
```

### export path

In the `default.ini` file setup export path by:

- Creating a `datasets` directory at the desired path.

- Place the desired path address in the `default.ini` file under the `export` section. Do not add the `datasets` directory in the path address.

## How to use

### Start API

```bash
python3 server.py
```
