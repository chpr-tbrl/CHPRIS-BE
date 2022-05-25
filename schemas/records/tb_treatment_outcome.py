from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import ForeignKeyField
from peewee import BooleanField

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Tb_treatment_outcomes(BaseModel):
    tb_treatment_outcome_id = PrimaryKeyField()
    tb_treatment_outcome_records_id = ForeignKeyField(Records)
    tb_treatment_outcome_date = DateTimeField(default=datetime.now)
    tb_treatment_outcome_user_id = IntegerField()
    tb_treatment_outcome_result = CharField() # ["cured", "treatment_completed", "lost_to_follow_up", "died", "transferred_out"]
    tb_treatment_outcome_comments = CharField(null=True)
    tb_treatment_outcome_close_patient_file = BooleanField(null=True)