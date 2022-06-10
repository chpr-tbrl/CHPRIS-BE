from peewee import CharField
from peewee import DateTimeField
from peewee import BooleanField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import DateField

from schemas.records.baseModel import BaseModel
from datetime import datetime

class Records(BaseModel):
    record_id = PrimaryKeyField()
    site_id = IntegerField()
    region_id = IntegerField()
    records_user_id = IntegerField()
    records_date = DateTimeField(default=datetime.now)
    records_name = CharField()
    records_age = IntegerField()
    records_sex = CharField()
    records_date_of_test_request = DateField()
    records_address = CharField()
    records_telephone = CharField()
    records_telephone_2 = CharField(null=True)
    records_has_art_unique_code = CharField()
    records_art_unique_code = CharField()
    records_status = CharField()
    records_ward_bed_number = CharField()
    records_currently_pregnant = CharField()
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
    records_tb_treatment_history = CharField()
    records_tb_treatment_history_contact_of_tb_patient = CharField(null=True)
    iv = CharField()