from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import ForeignKeyField

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Outcome_recorded(BaseModel):
    outcome_recorded_id = PrimaryKeyField()
    outcome_recorded_records_id = ForeignKeyField(Records)
    outcome_recorded_date = DateTimeField(default=datetime.now)
    outcome_recorded_user_id = IntegerField()
    outcome_recorded_started_tb_treatment_outcome = CharField(null=True) # ["started_tb_treatment", "referred_for_treatment", "other"]
    outcome_recorded_tb_rx_number = CharField(null=True)
    outcome_recorded_other = CharField(null=True)
    outcome_recorded_comments = CharField(null=True)