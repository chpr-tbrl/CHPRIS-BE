import logging
logger = logging.getLogger(__name__)

import os
import csv
from datetime import datetime

from schemas.records.records import Records

def data_export(start_date:str, end_date:str, region_id:int = None, site_id:int = None) -> str:
    """
    """
    field_names = [
        'record_id',
        'site_id',
        'region_id',
        'records_user_id',
        'records_date',
        'records_name',
        'records_age',
        'records_sex',
        'records_date_of_test_request',
        'records_address',
        'records_telephone',
        'records_telephone_2',
        'records_has_art_unique_code',
        'records_art_unique_code',
        'records_status',
        'records_ward_bed_number',
        'records_currently_pregnant',
        'records_symptoms_current_cough',
        'records_symptoms_fever',
        'records_symptoms_night_sweats',
        'records_symptoms_weight_loss',
        'records_symptoms_none_of_the_above',
        'records_patient_category_hospitalized',
        'records_patient_category_child',
        'records_patient_category_to_initiate_art',
        'records_patient_category_on_art_symptomatic',
        'records_patient_category_outpatient',
        'records_patient_category_anc',
        'records_patient_category_diabetes_clinic',
        'records_patient_category_other',
        'records_reason_for_test_presumptive_tb',
        'records_tb_treatment_history',
        'records_tb_treatment_history_contact_of_tb_patient'
    ]


    if not os.path.exists("datasets/"):
            os.makedirs("datasets/")

    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")

    export_file = '%s_record_export.csv' % date_time
    export_filepath = os.path.abspath(os.path.join('datasets', export_file))
    
    logger.debug("Gathering data ...")
    records = Records.select().where(
        Records.records_date.between(start_date, end_date),
        Records.region_id == region_id,
        Records.site_id == site_id
        ).dicts()

    logger.debug("exporting data please wait ...")
    with open(export_filepath, 'w') as fh:
        writer = csv.DictWriter(fh, fieldnames=field_names)
        writer.writeheader()        
        for row in records:
            writer.writerow(row)
    
    logger.info("- Export complete")
    return "%s/%s" % ("downloads", export_file)