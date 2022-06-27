from peewee import CharField
from peewee import DateTimeField

from schemas.sites.baseModel import BaseModel
from datetime import datetime

class Regions(BaseModel):
    name = CharField(null=True, unique=True)
    createdAt = DateTimeField(null=True, default=datetime.now)