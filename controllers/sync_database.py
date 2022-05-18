import logging
logger = logging.getLogger(__name__)

from error import InternalServerError
from Configs import configuration
from contextlib import closing
from mysql.connector import connect, Error

from schemas.users.baseModel import users_db
from schemas.users.users import Users
from schemas.users.sessions import Sessions

from schemas.sites.baseModel import sites_db
from schemas.sites.sites import Sites
from schemas.sites.regions import Regions

from schemas.records.baseModel import records_db
from schemas.records.records import Records
from schemas.records.specimen_collection import Specimen_collection
from schemas.records.lab import Lab

config = configuration()
database = config["DATABASE"]

def create_database():
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
            create_users_db_query = f"CREATE DATABASE IF NOT EXISTS {database['MYSQL_USERS_DATABASE']};"
            create_sites_db_query = f"CREATE DATABASE IF NOT EXISTS {database['MYSQL_SITES_DATABASE']};"
            create_records_db_query = f"CREATE DATABASE IF NOT EXISTS {database['MYSQL_RECORDS_DATABASE']};"
            with closing(connection.cursor()) as cursor:
                logger.debug(f"Creating database {database['MYSQL_USERS_DATABASE']} ...")
                cursor.execute(create_users_db_query)
                logger.info(f"Database {database['MYSQL_USERS_DATABASE']} successfully created")

                logger.debug(f"Creating database {database['MYSQL_SITES_DATABASE']} ...")
                cursor.execute(create_sites_db_query)
                logger.info(f"Database {database['MYSQL_SITES_DATABASE']} successfully created")

                logger.debug(f"Creating database {database['MYSQL_RECORDS_DATABASE']} ...")
                cursor.execute(create_records_db_query)
                logger.info(f"Database {database['MYSQL_RECORDS_DATABASE']} successfully created")

    except Error as error:
        raise InternalServerError(error)
    except Exception as error:
        raise InternalServerError(error)

def create_tables():
    try:
        # create users database tables
        logger.debug(f"Syncing database {database['MYSQL_USERS_DATABASE']} ...")
        users_db.create_tables(
            [
                Users, 
                Sessions
            ]
        )

        logger.info(f"Successfully Sync database {database['MYSQL_USERS_DATABASE']}")

        # create sites database tables
        logger.debug(f"Syncing database {database['MYSQL_SITES_DATABASE']} ...")
        sites_db.create_tables(
            [
                Sites, 
                Regions
            ]
        )

        logger.info(f"Successfully Sync database {database['MYSQL_SITES_DATABASE']}")

        # create records database tables
        logger.debug(f"Syncing database {database['MYSQL_RECORDS_DATABASE']} ...")
        records_db.create_tables(
            [
                Records,
                Specimen_collection,
                Lab
            ]
        )

        logger.info(f"Successfully Sync database {database['MYSQL_RECORDS_DATABASE']}")
    except Exception as error:
        raise InternalServerError(error)