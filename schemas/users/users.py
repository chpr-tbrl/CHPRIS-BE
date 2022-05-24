from peewee import (
    CharField,
    DateTimeField,
    TextField
)
from schemas.users.baseModel import BaseModel
from datetime import datetime

class Users(BaseModel):
    email = CharField(null=True, unique=True)
    password = CharField(null=True)
    phone_number = CharField(null=True)
    name = CharField(null=True)
    region = CharField(null=True)
    occupation = CharField(null=True)
    site = CharField(null=True)
    state = CharField(null=True, default="pending")
    type_of_user = CharField(null=True, default="data_collection")
    type_of_export = TextField(null=True)
    last_login = DateTimeField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)