from Configs import baseConfig
config = baseConfig()
database = config["DATABASE"]

from peewee import MySQLDatabase
from peewee import Model
from peewee import DatabaseError

from werkzeug.exceptions import InternalServerError

try:
    sites_db = MySQLDatabase(
        database["MYSQL_SITES_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(Model):
        """
        Sites database model.
        """
        class Meta:
            database = sites_db

except DatabaseError as error:
    raise InternalServerError(error)
