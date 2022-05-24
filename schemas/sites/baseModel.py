from error import InternalServerError
from Configs import baseConfig
from peewee import MySQLDatabase, Model
from peewee import DatabaseError

config = baseConfig()
database = config["DATABASE"]

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
