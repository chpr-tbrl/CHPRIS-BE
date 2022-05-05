import logging
logger = logging.getLogger(__name__)

from error import InternalServerError
from Configs import configuration
from contextlib import closing
from mysql.connector import connect, Error

from schemas.users.baseModel import users_db
from schemas import Users
from schemas import Sessions

from schemas.sites.baseModel import sites_db
from schemas import Sites
from schemas import Regions

config = configuration()
usersDatabase = config["USERS_DATABASE"]
sitesDatabase = config["SITES_DATABASE"]

def create_database():
    try:
        # create users database
        with closing(
            connect(
                user=usersDatabase["MYSQL_USER"],
                password=usersDatabase["MYSQL_PASSWORD"],
                host=usersDatabase["MYSQL_HOST"],
                auth_plugin="mysql_native_password",
            )
        ) as connection:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {usersDatabase['MYSQL_DATABASE']};"
            with closing(connection.cursor()) as cursor:
                logger.debug(f"Creating database {usersDatabase['MYSQL_DATABASE']} ...")
                cursor.execute(create_db_query)
                logger.info(f"Database {usersDatabase['MYSQL_DATABASE']} successfully created")

        # create sites database
        with closing(
            connect(
                user=sitesDatabase["MYSQL_USER"],
                password=sitesDatabase["MYSQL_PASSWORD"],
                host=sitesDatabase["MYSQL_HOST"],
                auth_plugin="mysql_native_password",
            )
        ) as connection:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {sitesDatabase['MYSQL_DATABASE']};"
            with closing(connection.cursor()) as cursor:
                logger.debug(f"Creating database {sitesDatabase['MYSQL_DATABASE']} ...")
                cursor.execute(create_db_query)
                logger.info(f"Database {sitesDatabase['MYSQL_DATABASE']} successfully created")
    except Error as error:
        raise InternalServerError(error)
    except Exception as error:
        raise InternalServerError(error)

def create_tables():
    try:
        # create users database tables
        logger.debug(f"Syncing database {usersDatabase['MYSQL_DATABASE']} ...")
        users_db.create_tables([Users, Sessions])

        logger.info(f"Successfully Sync database {usersDatabase['MYSQL_DATABASE']}")

        # create sites database tables
        logger.debug(f"Syncing database {sitesDatabase['MYSQL_DATABASE']} ...")
        sites_db.create_tables([Sites, Regions])

        logger.info(f"Successfully Sync database {sitesDatabase['MYSQL_DATABASE']}")
    except Exception as error:
        raise InternalServerError(error)