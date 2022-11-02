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
    lab_smear_microscopy_result_result_1 = CharField(null=True) 
    lab_smear_microscopy_result_result_2 = CharField(null=True) 
    lab_smear_microscopy_result_date = DateField(null=True)
    lab_smear_microscopy_result_done_by = CharField(null=True)
    lab_xpert_mtb_rif_assay_result = CharField(null=True) 
    lab_xpert_mtb_rif_assay_grades = CharField(null=True) 
    lab_xpert_mtb_rif_assay_rif_result = CharField(null=True) 
    lab_xpert_mtb_rif_assay_result_2 = CharField(null=True) 
    lab_xpert_mtb_rif_assay_grades_2 = CharField(null=True) 
    lab_xpert_mtb_rif_assay_rif_result_2 = CharField(null=True) 
    lab_xpert_mtb_rif_assay_date = DateField(null=True)
    lab_xpert_mtb_rif_assay_done_by = CharField(null=True)
    lab_urine_lf_lam_result = CharField(null=True) 
    lab_urine_lf_lam_date = DateField(null=True)
    lab_urine_lf_lam_done_by = CharField(null=True)
    lab_culture_mgit_culture = CharField(null=True)
    lab_culture_lj_culture = CharField(null=True)
    lab_culture_date = DateField(null=True)
    lab_culture_done_by = CharField(null=True)
    lab_lpa_mtbdrplus_isoniazid = CharField(null=True)
    lab_lpa_mtbdrplus_rifampin = CharField(null=True)
    lab_lpa_mtbdrs_flouoroquinolones = CharField(null=True)
    lab_lpa_mtbdrs_kanamycin = CharField(null=True)
    lab_lpa_mtbdrs_amikacin = CharField(null=True)
    lab_lpa_mtbdrs_capreomycin = CharField(null=True)
    lab_lpa_mtbdrs_low_level_kanamycin = CharField(null=True)
    lab_lpa_date = DateField(null=True)
    lab_lpa_done_by = CharField(null=True)
    lab_dst_isonazid = CharField(null=True)
    lab_dst_rifampin = CharField(null=True)
    lab_dst_ethambutol = CharField(null=True)
    lab_dst_kanamycin = CharField(null=True)
    lab_dst_ofloxacin = CharField(null=True)
    lab_dst_levofloxacinekanamycin = CharField(null=True)
    lab_dst_moxifloxacinekanamycin = CharField(null=True)    
    lab_dst_amikacinekanamycin = CharField(null=True)    
    lab_dst_date = DateField(null=True)    
    lab_dst_done_by = CharField(null=True)