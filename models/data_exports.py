import logging
logger = logging.getLogger(__name__)

import os
import csv
from datetime import datetime

from security.data import Data

from schemas.records.records import Records

from models.purge_exports import purge_export

from werkzeug.exceptions import InternalServerError

def data_export(start_date:str, end_date:str, permitted_decrypted_data: bool, region_id:str = None, site_id:str = None) -> str:
    """
    """
    try:
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
        if region_id == "all" and site_id == "all":
            records = Records.select().where(
                Records.records_date.between(start_date, end_date)
                ).dicts()        
        elif region_id == "all":
             records = Records.select().where(
                Records.records_date.between(start_date, end_date), 
                Records.site_id == site_id
                ).dicts()       
        elif site_id == "all":
             records = Records.select().where(
                Records.records_date.between(start_date, end_date), 
                Records.region_id == region_id
                ).dicts()        
        else:
            Records.select().where(
                Records.records_date.between(start_date, end_date),
                Records.region_id == region_id,
                Records.site_id == site_id
                ).dicts()

        logger.debug("exporting data please wait ...")
        with open(export_filepath, 'w') as fh:
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()        
            for row in records.iterator():
                if permitted_decrypted_data:
                    iv = row['iv']
                    data = Data()
                    writer.writerow({
                        'record_id':row['record_id'],
                        'site_id':row['site_id'],
                        'region_id':row['region_id'],
                        'records_user_id':row['records_user_id'],
                        'records_date':row['records_date'],
                        'records_name': data.decrypt(row['records_name'], iv),
                        'records_age':row['records_age'],
                        'records_sex':row['records_sex'],
                        'records_date_of_test_request':row['records_date_of_test_request'],
                        'records_address': data.decrypt(row['records_address'], iv),
                        'records_telephone': data.decrypt(row['records_telephone'], iv),
                        'records_telephone_2': data.decrypt(row['records_telephone_2'], iv),
                        'records_has_art_unique_code':row['records_has_art_unique_code'],
                        'records_art_unique_code': data.decrypt(row['records_art_unique_code'], iv),
                        'records_status':row['records_status'],
                        'records_ward_bed_number': data.decrypt(row['records_ward_bed_number'], iv),
                        'records_currently_pregnant':row['records_currently_pregnant'],
                        'records_symptoms_current_cough':row['records_symptoms_current_cough'],
                        'records_symptoms_fever':row['records_symptoms_fever'],
                        'records_symptoms_night_sweats':row['records_symptoms_night_sweats'],
                        'records_symptoms_weight_loss':row['records_symptoms_weight_loss'],
                        'records_symptoms_none_of_the_above':row['records_symptoms_none_of_the_above'],
                        'records_patient_category_hospitalized':row['records_patient_category_hospitalized'],
                        'records_patient_category_child':row['records_patient_category_child'],
                        'records_patient_category_to_initiate_art':row['records_patient_category_to_initiate_art'],
                        'records_patient_category_on_art_symptomatic':row['records_patient_category_on_art_symptomatic'],
                        'records_patient_category_outpatient':row['records_patient_category_outpatient'],
                        'records_patient_category_anc':row['records_patient_category_anc'],
                        'records_patient_category_diabetes_clinic':row['records_patient_category_diabetes_clinic'],
                        'records_patient_category_other':row['records_patient_category_other'],
                        'records_reason_for_test_presumptive_tb':row['records_reason_for_test_presumptive_tb'],
                        'records_tb_treatment_history':row['records_tb_treatment_history'],
                        'records_tb_treatment_history_contact_of_tb_patient': data.decrypt(row['records_tb_treatment_history_contact_of_tb_patient'], iv)
                    })
                else:
                    writer.writerow({
                        'record_id':row['record_id'],
                        'site_id':row['site_id'],
                        'region_id':row['region_id'],
                        'records_user_id':row['records_user_id'],
                        'records_date':row['records_date'],
                        'records_name':row['records_name'],
                        'records_age':row['records_age'],
                        'records_sex':row['records_sex'],
                        'records_date_of_test_request':row['records_date_of_test_request'],
                        'records_address':row['records_address'],
                        'records_telephone':row['records_telephone'],
                        'records_telephone_2':row['records_telephone_2'],
                        'records_has_art_unique_code':row['records_has_art_unique_code'],
                        'records_art_unique_code':row['records_art_unique_code'],
                        'records_status':row['records_status'],
                        'records_ward_bed_number':row['records_ward_bed_number'],
                        'records_currently_pregnant':row['records_currently_pregnant'],
                        'records_symptoms_current_cough':row['records_symptoms_current_cough'],
                        'records_symptoms_fever':row['records_symptoms_fever'],
                        'records_symptoms_night_sweats':row['records_symptoms_night_sweats'],
                        'records_symptoms_weight_loss':row['records_symptoms_weight_loss'],
                        'records_symptoms_none_of_the_above':row['records_symptoms_none_of_the_above'],
                        'records_patient_category_hospitalized':row['records_patient_category_hospitalized'],
                        'records_patient_category_child':row['records_patient_category_child'],
                        'records_patient_category_to_initiate_art':row['records_patient_category_to_initiate_art'],
                        'records_patient_category_on_art_symptomatic':row['records_patient_category_on_art_symptomatic'],
                        'records_patient_category_outpatient':row['records_patient_category_outpatient'],
                        'records_patient_category_anc':row['records_patient_category_anc'],
                        'records_patient_category_diabetes_clinic':row['records_patient_category_diabetes_clinic'],
                        'records_patient_category_other':row['records_patient_category_other'],
                        'records_reason_for_test_presumptive_tb':row['records_reason_for_test_presumptive_tb'],
                        'records_tb_treatment_history':row['records_tb_treatment_history'],
                        'records_tb_treatment_history_contact_of_tb_patient':row['records_tb_treatment_history_contact_of_tb_patient']
                    })

        logger.info("- Export complete")

        purge_export(max_days=7)

        return "%s/%s" % ("/downloads", export_file)

    except Exception as error:
        raise InternalServerError(error) from None