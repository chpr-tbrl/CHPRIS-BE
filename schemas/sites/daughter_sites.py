from peewee import ForeignKeyField
from peewee import DateTimeField

from schemas.sites.baseModel import BaseModel
from datetime import datetime

from schemas.sites.sites import Sites

class Daughter_sites(BaseModel):
    site_id = ForeignKeyField(Sites)
    daughter_site_id = ForeignKeyField(Sites)
    createdAt = DateTimeField(null=True, default=datetime.now)