from peewee import (
    CharField,
    DateTimeField,
    IntegerField,
    PrimaryKeyField,
    DateField,
    ForeignKeyField,
    BooleanField
)

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Follow_ups(BaseModel):
    follow_up_id = PrimaryKeyField()
    follow_up_records_id = ForeignKeyField(Records)
    follow_up_date = DateTimeField(default=datetime.now)
    follow_up_user_id = IntegerField()
    follow_up_xray = BooleanField(null=True)
    follow_up_amoxicillin = BooleanField(null=True)
    follow_up_other_antibiotic = CharField(null=True)
    follow_up_schedule_date = DateField() 
    follow_up_comments = CharField(null=True)