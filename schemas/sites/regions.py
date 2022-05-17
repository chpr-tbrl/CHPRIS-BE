from peewee import (
    CharField,
    DateTimeField
)
from schemas.sites.baseModel import BaseModel
from datetime import datetime

class Regions(BaseModel):
    name = CharField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now())