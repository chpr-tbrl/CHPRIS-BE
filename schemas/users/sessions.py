from peewee import CharField
from peewee import DateTimeField
from peewee import TextField

from schemas.users.baseModel import BaseModel

class Sessions(BaseModel):
    sid = CharField(primary_key=True)
    unique_identifier = CharField(null=True)
    user_agent = CharField(null=True)
    expires = DateTimeField(null=True)
    data = TextField(null=True)
    createdAt = DateTimeField(null=True)