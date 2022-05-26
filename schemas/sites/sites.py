from peewee import CharField
from peewee import ForeignKeyField
from peewee import DateTimeField

from schemas.sites.baseModel import BaseModel
from datetime import datetime

from schemas.sites.regions import Regions

class Sites(BaseModel):
    name = CharField(null=True)
    region_id = ForeignKeyField(Regions)
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        indexes = ((('name', 'region_id'), True),)