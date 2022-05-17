from error import InternalServerError
from Configs import configuration
from peewee import MySQLDatabase, Model
from peewee import DatabaseError

config = configuration()
database = config["DATABASE"]

try:
    records_db = MySQLDatabase(
        database["MYSQL_RECORDS_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(Model):
        class Meta:
            database = records_db

except DatabaseError as error:
    raise InternalServerError(error)
