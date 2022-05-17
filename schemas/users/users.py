from peewee import (
    CharField,
    DateTimeField
)
from schemas.users.baseModel import BaseModel
from datetime import datetime
from uuid import uuid1

class Users(BaseModel):
    id = CharField(primary_key=True, default=uuid1)
    email = CharField(null=True, unique=True)
    password = CharField(null=True)
    phone_number = CharField(null=True)
    name = CharField(null=True)
    region = CharField(null=True)
    occupation = CharField(null=True)
    site = CharField(null=True)
    state = CharField(null=True, default="pending")
    last_login = DateTimeField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now())