from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import DateField
from peewee import ForeignKeyField

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Labs(BaseModel):
    lab_id = PrimaryKeyField()
    lab_records_id = ForeignKeyField(Records)
    lab_date = DateTimeField(default=datetime.now)
    lab_user_id = IntegerField()
    lab_date_specimen_collection_received = DateField()
    lab_received_by = CharField()
    lab_registration_number = CharField()
    lab_smear_microscopy_result_result_1 = CharField(null=True) # ["no_afb_seen", "scanty", "1+", "2+", "3+", "tb_lamp_positive", "tb_lamp_negative", "not_done"]
    lab_smear_microscopy_result_result_2 = CharField(null=True) # ["no_afb_seen", "scanty", "1+", "2+", "3+", "tb_lamp_positive", "tb_lamp_negative", "not_done"]
    lab_smear_microscopy_result_date = DateField(null=True)
    lab_smear_microscopy_result_done_by = CharField(null=True)
    lab_xpert_mtb_rif_assay_result = CharField(null=True) # ["detected", "trace", "not_detected", "error_invalid", "not_done"]
    lab_xpert_mtb_rif_assay_grades = CharField(null=True) # ["high", "medium", "low", "very_low"]
    lab_xpert_mtb_rif_assay_rif_result = CharField(null=True) # ["detected", "indeterminate", "not_detected", "not_done"]
    lab_xpert_mtb_rif_assay_date = DateField(null=True)
    lab_xpert_mtb_rif_assay_done_by = CharField(null=True)
    lab_urine_lf_lam_result = CharField(null=True) # ["negative", "positive", "error_invalid", "not_done"]
    lab_urine_lf_lam_date = DateField(null=True)
    lab_urine_lf_lam_done_by = CharField(null=True)