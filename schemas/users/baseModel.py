from error import InternalServerError
from Configs import configuration
from peewee import Model, MySQLDatabase
from peewee import DatabaseError

config = configuration()
database = config["DATABASE"]

try:
    users_db = MySQLDatabase(
        database["MYSQL_USERS_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(Model):
        class Meta:
            database = users_db

except DatabaseError as error:
    raise InternalServerError(error)
