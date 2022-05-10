from importlib_metadata import email
import peewee as pw
from schemas.users.baseModel import BaseModel
from datetime import datetime
from uuid import uuid1

class Users(BaseModel):
    id = pw.CharField(primary_key=True, default=uuid1)
    email = pw.CharField(null=True, unique=True)
    password = pw.CharField(null=True)
    phone_number = pw.CharField(null=True)
    name = pw.CharField(null=True)
    region = pw.CharField(null=True)
    occupation = pw.CharField(null=True)
    site = pw.CharField(null=True)
    state = pw.CharField(null=True, default="pending")
    last_login = pw.DateTimeField(null=True)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())