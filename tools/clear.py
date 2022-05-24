#!/usr/bin/env python 

import os
import logging

from contextlib import closing
from mysql.connector import connect, Error

def delete_all_database(user: str, password: str) -> None:
    with closing(
        connect(
            user=user,
            password=password
        )
    ) as connection:
        user_db = "CHPRIS_BE_Users"
        site_db = "CHPRIS_BE_Sites"
        record_db = "CHPRIS_BE_Records"

        delete_users_db_query = "DROP DATABASE %s;" % user_db
        delete_sites_db_query = "DROP DATABASE %s;" % site_db
        delete_records_db_query = "DROP DATABASE %s;" % record_db
        with closing(connection.cursor()) as cursor:
            cursor.execute(delete_users_db_query)
            cursor.execute(delete_sites_db_query)
            cursor.execute(delete_records_db_query)
            
            logging.info("- Done")

if __name__ == "__main__":
    import argparse
    from getpass import getpass

    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", help="Delete all databases", action="store_true")
    args = parser.parse_args()

    if args.all:
        try:
            user = input("Username:")
            password = getpass()

            delete_all_database(user=user, password=password)
            logging.info("- Successfully deleted all databases")
        except Error as error:
            raise Exception(error)
        except Exception as error:
            raise Exception(error)