from Configs import baseConfig
config = baseConfig()
database = config["DATABASE"]

from peewee import Model
from peewee import MySQLDatabase
from peewee import DatabaseError

from werkzeug.exceptions import InternalServerError

try:
    users_db = MySQLDatabase(
        database["MYSQL_USERS_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(Model):
        """
        Users database model.
        """
        class Meta:
            database = users_db

except DatabaseError as error:
    raise InternalServerError(error)
