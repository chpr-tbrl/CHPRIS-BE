from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import DateField
from peewee import BooleanField
from playhouse.mysql_ext import JSONField

from schemas.users.baseModel import BaseModel
from datetime import datetime

class Users(BaseModel):
    email = CharField(unique=True)
    name = CharField()
    phone_number = CharField()
    occupation = CharField()
    password_hash = CharField()
    account_status = CharField(default="pending")
    account_type = CharField(default="data_collector")
    account_request_date = DateField(default=datetime.now)
    account_approved_date = DateField(null=True)
    permitted_export_types = JSONField(default=[])
    permitted_export_range = IntegerField(default=1)
    permitted_decrypted_data = BooleanField(default=False)
    permitted_approve_accounts = BooleanField(default=False)
    iv = CharField()
    createdAt = DateTimeField(default=datetime.now)