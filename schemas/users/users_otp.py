from random import randint

from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField

from schemas.users.baseModel import BaseModel
from datetime import datetime
from datetime import timedelta

def code():
    n = 6
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def expire():
    time = 5
    return datetime.now() + timedelta(minutes=time)

class Users_otp(BaseModel):
    phone_number = CharField()
    code = IntegerField(default=code)
    expires = DateTimeField(default=expire, null=True)
    status = CharField(default="pending", null=True)
    createdAt = DateTimeField(default=datetime.now)