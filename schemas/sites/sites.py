from peewee import CharField
from peewee import ForeignKeyField
from peewee import DateTimeField

from schemas.sites.baseModel import BaseModel
from datetime import datetime

from schemas.sites.regions import Regions

class Sites(BaseModel):
    name = CharField()
    region_id = ForeignKeyField(Regions)
    site_code = CharField()
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        indexes = ((('name', 'region_id'), True), (('site_code', 'region_id'), True),)