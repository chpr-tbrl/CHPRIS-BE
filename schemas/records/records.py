from peewee import (
    CharField,
    DateTimeField,
    BooleanField,
    IntegerField,
    PrimaryKeyField
)
from peewee_plus import EnumField

from schemas.records.baseModel import BaseModel
from datetime import datetime

class Records(BaseModel):
    record_id = PrimaryKeyField(primary_key=True)
    site_id = IntegerField()
    region_id = IntegerField()
    records_user_id = IntegerField()
    records_date = DateTimeField(default=datetime.now())
    records_name = CharField()
    records_age = IntegerField()
    records_sex = EnumField(["male", "female"])
    records_date_of_test_request = DateTimeField()
    records_address = CharField()
    records_telephone = CharField()
    records_telephone_2 = CharField(null=True)
    records_has_art_unique_code = EnumField(["yes", "no", "unknown"])
    records_art_unique_code = CharField()
    records_status = EnumField(["outpatient", "ward-bed"])
    records_ward_bed_number = CharField()
    records_currently_pregnant = EnumField(["yes", "no"])
    records_symptoms_current_cough = BooleanField(null=True)
    records_symptoms_fever = BooleanField(null=True)
    records_symptoms_night_sweats = BooleanField(null=True)
    records_symptoms_weight_loss = BooleanField(null=True)
    records_symptoms_none_of_the_above = BooleanField()
    records_patient_category_hospitalized = BooleanField(null=True)
    records_patient_category_child = BooleanField(null=True)
    records_patient_category_to_initiate_art = BooleanField(null=True)
    records_patient_category_on_art_symptomatic = BooleanField(null=True)
    records_patient_category_outpatient = BooleanField(null=True)
    records_patient_category_anc = BooleanField(null=True)
    records_patient_category_diabetes_clinic = BooleanField(null=True)
    records_patient_category_other = CharField(null=True)
    records_reason_for_test_presumptive_tb = BooleanField(null=True)
    records_tb_treatment_history = EnumField(["new", "relapse", "after_loss_to_follow_up", "failure"])
    records_tb_treatment_history_contact_of_tb_patient = CharField(null=True)