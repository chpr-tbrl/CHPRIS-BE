from importlib_metadata import email
import peewee as pw
from schemas.users.baseModel import BaseModel
from datetime import datetime
from uuid import uuid1

class Users(BaseModel):
    id = pw.CharField(primary_key=True, default=uuid1)
    email = pw.CharField(null=True)
    password = pw.CharField(null=True)
    last_login = pw.DateTimeField(null=True)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())