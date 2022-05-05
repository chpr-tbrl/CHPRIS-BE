import peewee as pw
from schemas.sites.baseModel import BaseModel
from datetime import datetime

class Regions(BaseModel):
    name = pw.CharField(null=True)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())