from error import InternalServerError
from Configs import configuration
import peewee as pw

config = configuration()
database = config["USERS_DATABASE"]

try:
    users_db = pw.MySQLDatabase(
        database["MYSQL_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(pw.Model):
        class Meta:
            database = users_db

except pw.DatabaseError as error:
    raise InternalServerError(error)
