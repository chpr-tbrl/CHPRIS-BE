from peewee import CharField
from peewee import DateTimeField
from peewee import TextField
from peewee import IntegerField

from schemas.users.baseModel import BaseModel
from datetime import datetime

class Users(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    phone_number = CharField(null=True)
    name = CharField(null=True)
    occupation = CharField(null=True)
    state = CharField(default="pending")
    type_of_user = CharField(default="data_collection")
    type_of_export = TextField(null=True)
    exportable_range = IntegerField(null=True)
    region_id = IntegerField()
    site_id = IntegerField()
    createdAt = DateTimeField(null=True, default=datetime.now)