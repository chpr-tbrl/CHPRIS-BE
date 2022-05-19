from peewee import (
    CharField,
    ForeignKeyField, 
    DateTimeField
)
from schemas.sites.baseModel import BaseModel
from datetime import datetime

from schemas.sites.regions import Regions

class Sites(BaseModel):
    name = CharField(null=True)
    region = ForeignKeyField(Regions)
    createdAt = DateTimeField(null=True, default=datetime.now)