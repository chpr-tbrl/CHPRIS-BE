import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
database = config["DATABASE"]

from peewee import Model
from peewee import MySQLDatabase
from peewee import DatabaseError

from werkzeug.exceptions import InternalServerError

try:
    logger.debug("connecting to %s database ..." % database["MYSQL_USERS_DATABASE"])

    users_db = MySQLDatabase(
        database["MYSQL_USERS_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    logger.info("- Successfully connected to %s database" % database["MYSQL_USERS_DATABASE"])
except DatabaseError as error:
    raise InternalServerError(error)

class BaseModel(Model):
    """
    Users database model.
    """
    class Meta:
        database = users_db