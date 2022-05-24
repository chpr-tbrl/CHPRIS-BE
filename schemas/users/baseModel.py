from error import InternalServerError
from Configs import baseConfig
from peewee import Model, MySQLDatabase
from peewee import DatabaseError

config = baseConfig()
database = config["DATABASE"]

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
