import logging
logger = logging.getLogger(__name__)

from security.data import Data

from schemas.records.records import Records
from schemas.records.specimen_collection import Specimen_collections
from schemas.records.lab import Labs
from schemas.records.follow_up import Follow_ups
from schemas.records.outcome_recorded import Outcome_recorded
from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

import os
import csv
from datetime import datetime
from datetime import timedelta

from werkzeug.exceptions import InternalServerError

class Export_Model:
    def __init__(self) -> None:
        """
        """
        self.Records = Records
        self.Specimen_collections = Specimen_collections
        self.Labs = Labs
        self.Follow_ups = Follow_ups
        self.Outcome_recorded = Outcome_recorded
        self.Tb_treatment_outcomes = Tb_treatment_outcomes
        self.Data = Data

    def records(self, start_date:str, end_date:str, permitted_decrypted_data: bool, region_id:str = None, site_id:str = None) -> str:
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
                'records_tb_treatment_history_contact_of_tb_patient',
                'records_tb_type',
                'records_tb_treatment_number',
                'records_sms_notifications',

                'specimen_collection_user_id',
                'specimen_collection_1_date',
                'specimen_collection_1_specimen_collection_type',
                'specimen_collection_1_other',
                'specimen_collection_1_period',
                'specimen_collection_1_aspect',
                'specimen_collection_1_received_by',
                'specimen_collection_2_date',
                'specimen_collection_2_specimen_collection_type',
                'specimen_collection_2_other',
                'specimen_collection_2_period',
                'specimen_collection_2_aspect',
                'specimen_collection_2_received_by',

                'lab_user_id',
                'lab_date_specimen_collection_received',
                'lab_received_by',
                'lab_registration_number',
                'lab_smear_microscopy_result_result_1',
                'lab_smear_microscopy_result_result_2',
                'lab_smear_microscopy_result_date',
                'lab_smear_microscopy_result_done_by',
                'lab_xpert_mtb_rif_assay_result',
                'lab_xpert_mtb_rif_assay_grades',
                'lab_xpert_mtb_rif_assay_rif_result',
                'lab_xpert_mtb_rif_assay_date',
                'lab_xpert_mtb_rif_assay_done_by',
                'lab_urine_lf_lam_result',
                'lab_urine_lf_lam_date',
                'lab_urine_lf_lam_done_by',

                'follow_up_user_id',
                'follow_up_xray',
                'follow_up_amoxicillin',
                'follow_up_other_antibiotic',
                'follow_up_schedule_date',
                'follow_up_comments',

                'outcome_recorded_user_id',
                'outcome_recorded_started_tb_treatment_outcome',
                'outcome_recorded_tb_rx_number',
                'outcome_recorded_other',
                'outcome_recorded_comments',

                'tb_treatment_outcome_user_id',
                'tb_treatment_outcome_result',
                'tb_treatment_outcome_comments',
                'tb_treatment_outcome_close_patient_file',
            ]

            if not os.path.exists("datasets/"):
                    os.makedirs("datasets/")

            now = datetime.now()
            date_time = now.strftime("%m-%d-%Y-%H:%M:%S")

            export_file = '%s_record_export.csv' % date_time
            export_filepath = os.path.abspath(os.path.join('datasets', export_file))
            
            logger.debug("Gathering data ...")
            if region_id == "all" and site_id == "all":
                records = self.Records.select().where(
                    self.Records.records_date.between(start_date, end_date)
                    ).dicts()        
            elif region_id == "all":
                records = self.Records.select().where(
                    self.Records.records_date.between(start_date, end_date), 
                    self.Records.site_id == site_id
                    ).dicts()       
            elif site_id == "all":
                records = self.Records.select().where(
                    self.Records.records_date.between(start_date, end_date), 
                    self.Records.region_id == region_id
                    ).dicts()        
            else:
                records = self.Records.select().where(
                    self.Records.records_date.between(start_date, end_date),
                    self.Records.region_id == region_id,
                    self.Records.site_id == site_id
                    ).dicts()

            logger.debug("exporting data please wait ...")

            with open(export_filepath, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()        

                for row in records.iterator():
                    # specimen_collections
                    specimen_collections_results = []

                    specimen_collections = (
                        self.Specimen_collections.select()
                        .where(self.Specimen_collections.specimen_collection_records_id == row['record_id'])
                        .dicts()
                    )

                    for specimen_collection in specimen_collections:
                        specimen_collections_results.append(specimen_collection)
            
                    # labs
                    labs_results = []

                    labs = (
                        self.Labs.select()
                        .where(self.Labs.lab_records_id == row['record_id'])
                        .dicts()
                    )

                    for lab in labs:
                        labs_results.append(lab)

                    # follow_ups
                    follow_ups_results = []
    
                    follow_ups = (
                        self.Follow_ups.select()
                        .where(self.Follow_ups.follow_up_records_id == row['record_id'])
                        .dicts()
                    )

                    for follow_up in follow_ups:
                        follow_ups_results.append(follow_up)

                    # outcomes_recorded
                    outcomes_recorded_results = []
            
                    outcomes_recorded = (
                        self.Outcome_recorded.select()
                        .where(self.Outcome_recorded.outcome_recorded_records_id == row['record_id'])
                        .dicts()
                    )

                    for outcome_recorded in outcomes_recorded:
                        outcomes_recorded_results.append(outcome_recorded)

                    # tb_treatment_outcomes
                    tb_treatment_outcomes_results = []
            
                    tb_treatment_outcomes = (
                        self.Tb_treatment_outcomes.select()
                        .where(self.Tb_treatment_outcomes.tb_treatment_outcome_records_id == row['record_id'])
                        .dicts()
                    )

                    for tb_treatment_outcome in tb_treatment_outcomes:
                        tb_treatment_outcomes_results.append(tb_treatment_outcome)

                    if permitted_decrypted_data:
                        iv = row['iv']

                        data = self.Data()

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
                            'records_tb_treatment_history_contact_of_tb_patient': data.decrypt(row['records_tb_treatment_history_contact_of_tb_patient'], iv),
                            'records_tb_type':row['records_tb_type'],
                            'records_tb_treatment_number':row['records_tb_treatment_number'],
                            'records_sms_notifications':row['records_sms_notifications'],

                            'specimen_collection_user_id': specimen_collections_results[0]['specimen_collection_user_id'],
                            'specimen_collection_1_date': specimen_collections_results[0]['specimen_collection_1_date'],
                            'specimen_collection_1_specimen_collection_type': specimen_collections_results[0]['specimen_collection_1_specimen_collection_type'],
                            'specimen_collection_1_other': specimen_collections_results[0]['specimen_collection_1_other'],
                            'specimen_collection_1_period': specimen_collections_results[0]['specimen_collection_1_period'],
                            'specimen_collection_1_aspect': specimen_collections_results[0]['specimen_collection_1_aspect'],
                            'specimen_collection_1_received_by': specimen_collections_results[0]['specimen_collection_1_received_by'],
                            'specimen_collection_2_date': specimen_collections_results[0]['specimen_collection_2_date'],
                            'specimen_collection_2_specimen_collection_type': specimen_collections_results[0]['specimen_collection_2_specimen_collection_type'],
                            'specimen_collection_2_other': specimen_collections_results[0]['specimen_collection_2_other'],
                            'specimen_collection_2_period': specimen_collections_results[0]['specimen_collection_2_period'],
                            'specimen_collection_2_aspect': specimen_collections_results[0]['specimen_collection_2_aspect'],
                            'specimen_collection_2_received_by': specimen_collections_results[0]['specimen_collection_2_received_by'],

                            'lab_user_id': labs_results[0]['lab_user_id'],
                            'lab_date_specimen_collection_received': labs_results[0]['lab_date_specimen_collection_received'],
                            'lab_received_by': labs_results[0]['lab_received_by'],
                            'lab_registration_number': labs_results[0]['lab_registration_number'],
                            'lab_smear_microscopy_result_result_1': labs_results[0]['lab_smear_microscopy_result_result_1'],
                            'lab_smear_microscopy_result_result_2': labs_results[0]['lab_smear_microscopy_result_result_2'],
                            'lab_smear_microscopy_result_date': labs_results[0]['lab_smear_microscopy_result_date'],
                            'lab_smear_microscopy_result_done_by': labs_results[0]['lab_smear_microscopy_result_done_by'],
                            'lab_xpert_mtb_rif_assay_result': labs_results[0]['lab_xpert_mtb_rif_assay_result'],
                            'lab_xpert_mtb_rif_assay_grades': labs_results[0]['lab_xpert_mtb_rif_assay_grades'],
                            'lab_xpert_mtb_rif_assay_rif_result': labs_results[0]['lab_xpert_mtb_rif_assay_rif_result'],
                            'lab_xpert_mtb_rif_assay_date': labs_results[0]['lab_xpert_mtb_rif_assay_date'],
                            'lab_xpert_mtb_rif_assay_done_by': labs_results[0]['lab_xpert_mtb_rif_assay_done_by'],
                            'lab_urine_lf_lam_result': labs_results[0]['lab_urine_lf_lam_result'],
                            'lab_urine_lf_lam_date': labs_results[0]['lab_urine_lf_lam_date'],
                            'lab_urine_lf_lam_done_by': labs_results[0]['lab_urine_lf_lam_done_by'],

                            'follow_up_user_id': follow_ups_results[0]['follow_up_user_id'],
                            'follow_up_xray': follow_ups_results[0]['follow_up_xray'],
                            'follow_up_amoxicillin': follow_ups_results[0]['follow_up_amoxicillin'],
                            'follow_up_other_antibiotic': follow_ups_results[0]['follow_up_other_antibiotic'],
                            'follow_up_schedule_date': follow_ups_results[0]['follow_up_schedule_date'],
                            'follow_up_comments': follow_ups_results[0]['follow_up_comments'],

                            'outcome_recorded_user_id': outcomes_recorded_results[0]['outcome_recorded_user_id'],
                            'outcome_recorded_started_tb_treatment_outcome': outcomes_recorded_results[0]['outcome_recorded_started_tb_treatment_outcome'],
                            'outcome_recorded_tb_rx_number': outcomes_recorded_results[0]['outcome_recorded_tb_rx_number'],
                            'outcome_recorded_other': outcomes_recorded_results[0]['outcome_recorded_other'],
                            'outcome_recorded_comments': outcomes_recorded_results[0]['outcome_recorded_comments'],

                            'tb_treatment_outcome_user_id': tb_treatment_outcomes_results[0]['tb_treatment_outcome_user_id'],
                            'tb_treatment_outcome_result': tb_treatment_outcomes_results[0]['tb_treatment_outcome_result'],
                            'tb_treatment_outcome_comments': tb_treatment_outcomes_results[0]['tb_treatment_outcome_comments'],
                            'tb_treatment_outcome_close_patient_file': tb_treatment_outcomes_results[0]['tb_treatment_outcome_close_patient_file']
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
                            'records_tb_treatment_history_contact_of_tb_patient':row['records_tb_treatment_history_contact_of_tb_patient'],
                            'records_tb_type':row['records_tb_type'],
                            'records_tb_treatment_number':row['records_tb_treatment_number'],
                            'records_sms_notifications':row['records_sms_notifications'],

                            'specimen_collection_user_id': specimen_collections_results[0]['specimen_collection_user_id'],
                            'specimen_collection_1_date': specimen_collections_results[0]['specimen_collection_1_date'],
                            'specimen_collection_1_specimen_collection_type': specimen_collections_results[0]['specimen_collection_1_specimen_collection_type'],
                            'specimen_collection_1_other': specimen_collections_results[0]['specimen_collection_1_other'],
                            'specimen_collection_1_period': specimen_collections_results[0]['specimen_collection_1_period'],
                            'specimen_collection_1_aspect': specimen_collections_results[0]['specimen_collection_1_aspect'],
                            'specimen_collection_1_received_by': specimen_collections_results[0]['specimen_collection_1_received_by'],
                            'specimen_collection_2_date': specimen_collections_results[0]['specimen_collection_2_date'],
                            'specimen_collection_2_specimen_collection_type': specimen_collections_results[0]['specimen_collection_2_specimen_collection_type'],
                            'specimen_collection_2_other': specimen_collections_results[0]['specimen_collection_2_other'],
                            'specimen_collection_2_period': specimen_collections_results[0]['specimen_collection_2_period'],
                            'specimen_collection_2_aspect': specimen_collections_results[0]['specimen_collection_2_aspect'],
                            'specimen_collection_2_received_by': specimen_collections_results[0]['specimen_collection_2_received_by'],

                            'lab_user_id': labs_results[0]['lab_user_id'],
                            'lab_date_specimen_collection_received': labs_results[0]['lab_date_specimen_collection_received'],
                            'lab_received_by': labs_results[0]['lab_received_by'],
                            'lab_registration_number': labs_results[0]['lab_registration_number'],
                            'lab_smear_microscopy_result_result_1': labs_results[0]['lab_smear_microscopy_result_result_1'],
                            'lab_smear_microscopy_result_result_2': labs_results[0]['lab_smear_microscopy_result_result_2'],
                            'lab_smear_microscopy_result_date': labs_results[0]['lab_smear_microscopy_result_date'],
                            'lab_smear_microscopy_result_done_by': labs_results[0]['lab_smear_microscopy_result_done_by'],
                            'lab_xpert_mtb_rif_assay_result': labs_results[0]['lab_xpert_mtb_rif_assay_result'],
                            'lab_xpert_mtb_rif_assay_grades': labs_results[0]['lab_xpert_mtb_rif_assay_grades'],
                            'lab_xpert_mtb_rif_assay_rif_result': labs_results[0]['lab_xpert_mtb_rif_assay_rif_result'],
                            'lab_xpert_mtb_rif_assay_date': labs_results[0]['lab_xpert_mtb_rif_assay_date'],
                            'lab_xpert_mtb_rif_assay_done_by': labs_results[0]['lab_xpert_mtb_rif_assay_done_by'],
                            'lab_urine_lf_lam_result': labs_results[0]['lab_urine_lf_lam_result'],
                            'lab_urine_lf_lam_date': labs_results[0]['lab_urine_lf_lam_date'],
                            'lab_urine_lf_lam_done_by': labs_results[0]['lab_urine_lf_lam_done_by'],

                            'follow_up_user_id': follow_ups_results[0]['follow_up_user_id'],
                            'follow_up_xray': follow_ups_results[0]['follow_up_xray'],
                            'follow_up_amoxicillin': follow_ups_results[0]['follow_up_amoxicillin'],
                            'follow_up_other_antibiotic': follow_ups_results[0]['follow_up_other_antibiotic'],
                            'follow_up_schedule_date': follow_ups_results[0]['follow_up_schedule_date'],
                            'follow_up_comments': follow_ups_results[0]['follow_up_comments'],

                            'outcome_recorded_user_id': outcomes_recorded_results[0]['outcome_recorded_user_id'],
                            'outcome_recorded_started_tb_treatment_outcome': outcomes_recorded_results[0]['outcome_recorded_started_tb_treatment_outcome'],
                            'outcome_recorded_tb_rx_number': outcomes_recorded_results[0]['outcome_recorded_tb_rx_number'],
                            'outcome_recorded_other': outcomes_recorded_results[0]['outcome_recorded_other'],
                            'outcome_recorded_comments': outcomes_recorded_results[0]['outcome_recorded_comments'],

                            'tb_treatment_outcome_user_id': tb_treatment_outcomes_results[0]['tb_treatment_outcome_user_id'],
                            'tb_treatment_outcome_result': tb_treatment_outcomes_results[0]['tb_treatment_outcome_result'],
                            'tb_treatment_outcome_comments': tb_treatment_outcomes_results[0]['tb_treatment_outcome_comments'],
                            'tb_treatment_outcome_close_patient_file': tb_treatment_outcomes_results[0]['tb_treatment_outcome_close_patient_file']
                        })

            logger.info("- Export complete")

            self.purge(max_days=7)

            return "%s/%s" % ("/downloads", export_file)

        except Exception as error:
            raise InternalServerError(error) from None

    def purge(self, max_days:int) -> None:
        """
        """
        try:
            logger.debug("removing export files older than %d day(s) ..." % max_days)

            export_filepath = os.path.abspath('datasets')
            date_limit = datetime.now() - timedelta(max_days)
            files = os.listdir(export_filepath)

            for file in files:
                file_path = os.path.abspath(os.path.join("datasets", file))
                filetime = datetime.fromtimestamp(os.path.getctime(file_path))
            
                if filetime < date_limit:
                    os.remove(file_path)
                    logger.info("- '%s' removed. Created: %s" % (file, filetime))

        except Exception as error:
            raise InternalServerError(error) from None