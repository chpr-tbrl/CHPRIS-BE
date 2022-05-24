#!/usr/bin/env python 

import os
import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

config_filepath = os.path.abspath("configs/default.ini")

if not os.path.exists(config_filepath):
    error = "configs file not found at %s" % config_filepath
    raise logger.exception(error)

config = ConfigParser()
config.read(config_filepath)

from contextlib import closing
from mysql.connector import connect, Error

database = config["DATABASE"]

def delete_all_database():
    try:
        # create users database
        with closing(
            connect(
                user=database["MYSQL_USER"],
                password=database["MYSQL_PASSWORD"],
                host=database["MYSQL_HOST"],
                auth_plugin="mysql_native_password",
            )
        ) as connection:
            delete_users_db_query = "DROP DATABASE %s;" % database['MYSQL_USERS_DATABASE']
            delete_sites_db_query = "DROP DATABASE %s;" % database['MYSQL_SITES_DATABASE']
            delete_records_db_query = "DROP DATABASE %s;" % database['MYSQL_RECORDS_DATABASE']
            with closing(connection.cursor()) as cursor:
                logger.debug("Deleting database %s ..." % database['MYSQL_USERS_DATABASE'])
                cursor.execute(delete_users_db_query)
                logger.info("Database %s successfully deleted" % database['MYSQL_USERS_DATABASE'])

                logger.debug("Deleting database %s ..." % database['MYSQL_SITES_DATABASE'])
                cursor.execute(delete_sites_db_query)
                logger.info("Database %s successfully deleted" % database['MYSQL_SITES_DATABASE'])

                logger.debug("Deleting database %s ..." % database['MYSQL_RECORDS_DATABASE'])
                cursor.execute(delete_records_db_query)
                logger.info("Database %s successfully deleted" % database['MYSQL_RECORDS_DATABASE'])

    except Error as error:
        raise logger.exception(error)
    except Exception as error:
        raise logger.exception(error)

if __name__ == "__main__":
    import argparse

    loglevel = os.getenv("--logs") or "info"
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % loglevel)
    
    logging.basicConfig(level=numeric_level)

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", help="Delete all databases", action="store_true")
    args = parser.parse_args()

    if args.all:
        delete_all_database()
        logger.info("- Successfully deleted all databases")