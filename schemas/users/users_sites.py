from peewee import ForeignKeyField
from peewee import DateTimeField
from peewee import IntegerField

from schemas.users.baseModel import BaseModel
from datetime import datetime

from schemas.users.users import Users

class Users_sites(BaseModel):
    user_id = ForeignKeyField(Users)
    site_id = IntegerField()
    createdAt = DateTimeField(default=datetime.now)