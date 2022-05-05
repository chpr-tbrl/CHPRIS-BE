import peewee as pw
from schemas.sites.baseModel import BaseModel
from datetime import datetime

from schemas.sites.regions import Regions

class Sites(BaseModel):
    name = pw.CharField(null=True)
    region = pw.ForeignKeyField(Regions)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())