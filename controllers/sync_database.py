import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
database = config["DATABASE"]

import os
import json
from contextlib import closing
from mysql.connector import connect
from mysql.connector import Error

from schemas.users.baseModel import users_db
from schemas.users.users import Users
from schemas.users.sessions import Sessions

from schemas.sites.baseModel import sites_db
from schemas.sites.sites import Sites
from schemas.sites.regions import Regions
from schemas.sites.daughter_sites import Daughter_sites

from schemas.records.baseModel import records_db
from schemas.records.records import Records
from schemas.records.specimen_collection import Specimen_collections
from schemas.records.lab import Labs
from schemas.records.follow_up import Follow_ups
from schemas.records.outcome_recorded import Outcome_recorded
from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

from werkzeug.exceptions import InternalServerError

def create_database() -> None:
    """
    Create all databases.

    Arguments:
        None

    Returns:
        None
    """
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
            create_users_db_query = "CREATE DATABASE IF NOT EXISTS %s;" % database['MYSQL_USERS_DATABASE']
            create_sites_db_query = "CREATE DATABASE IF NOT EXISTS %s;" % database['MYSQL_SITES_DATABASE']
            create_records_db_query = "CREATE DATABASE IF NOT EXISTS %s;" % database['MYSQL_RECORDS_DATABASE']
            with closing(connection.cursor()) as cursor:
                logger.debug("Creating database %s ..." % database['MYSQL_USERS_DATABASE'])
                cursor.execute(create_users_db_query)
                logger.info("- Database %s successfully created" % database['MYSQL_USERS_DATABASE'])

                logger.debug("Creating database %s ..." % database['MYSQL_SITES_DATABASE'])
                cursor.execute(create_sites_db_query)
                logger.info("- Database %s successfully created" % database['MYSQL_SITES_DATABASE'])

                logger.debug("Creating database %s ..." % database['MYSQL_RECORDS_DATABASE'])
                cursor.execute(create_records_db_query)
                logger.info("- Database %s successfully created" % database['MYSQL_RECORDS_DATABASE'])

    except Error as error:
        raise InternalServerError(error)
    except Exception as error:
        raise InternalServerError(error)

def create_tables() -> None:
    """
    Create all database tables.

    Arguments:
        None

    Returns:
        None
    """
    try:
        # create users database tables
        logger.debug("Syncing database %s ..." % database['MYSQL_USERS_DATABASE'])
        users_db.create_tables(
            [
                Users, 
                Sessions
            ]
        )

        logger.info("- Successfully Sync database %s" % database['MYSQL_USERS_DATABASE'])

        # create sites database tables
        logger.debug("Syncing database %s ..." % database['MYSQL_SITES_DATABASE'])
        sites_db.create_tables(
            [
                Sites, 
                Regions,
                Daughter_sites
            ]
        )

        logger.info("- Successfully Sync database %s" % database['MYSQL_SITES_DATABASE'])

        # create records database tables
        logger.debug("Syncing database %s ..." % database['MYSQL_RECORDS_DATABASE'])
        records_db.create_tables(
            [
                Records,
                Specimen_collections,
                Labs,
                Follow_ups,
                Outcome_recorded,
                Tb_treatment_outcomes
            ]
        )

        logger.info("- Successfully Sync database %s" % database['MYSQL_RECORDS_DATABASE'])
    except Exception as error:
        raise InternalServerError(error)

def sync_sites() -> None:
    """
    """
    try:
        sites_info_filepath = os.path.abspath("sites_info.json")
        regions_info_filepath = os.path.abspath("regions_info.json")

        if not os.path.exists(sites_info_filepath):
            error = f"Sites information file not found at {sites_info_filepath}"
            raise InternalServerError(error)

        if not os.path.exists(regions_info_filepath):
            error = f"Regions information file not found at {regions_info_filepath}"
            raise InternalServerError(error)


        with open(regions_info_filepath) as data_file:
            data = json.load(data_file)
            for region in data:
                try:
                    Regions.get(Regions.name == region["name"])
                except Regions.DoesNotExist:
                    Regions.create(
                        name=region["name"]
                    )

        with open(sites_info_filepath) as data_file:
            data = json.load(data_file)
            for site in data:
                try:
                    Sites.get(Sites.name == site["name"])
                except Sites.DoesNotExist:
                    Sites.create(
                        name=site["name"],
                        region_id=site["region_id"]
                    )

        try:
            Users.get(Users.email == "developers@afkanerd.com")
        except Users.DoesNotExist:
            from security.data import Data
            data = Data()
            Users.create(
                email="developers@afkanerd.com",
                password=data.hash("asshole"),
                state="verified",
                exportable_range=12,
                type_of_export="csv,pdf",
                type_of_user="admin",
                phone_number="+237123456",
                name="afkanerd_developer",
                region_id=1,
                occupation="developer",
                site_id=1
            )
    except Exception as error:
        raise InternalServerError(error)