import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.records import Records

logger = logging.getLogger(__name__)

def get_all_records():
    try:
        logger.debug(f"fetching all records ...")
        result = []
        
        records = (
            Records.select()
            .dicts()
        )
        for record in records:
            result.append({
                "record_id":record["record_id"],
                "records_date":record["records_date"],
                "site_id":record["site_id,"],
                "region_id":record["region_id,"],
                "records_user_id":record["records_user_id,"],
                "records_name":record["records_name,"],
                "records_age":record["records_age,"],
                "records_sex":record["records_sex,"],
                "records_date_of_test_request":record["records_date_of_test_request,"],
                "records_address":record["records_address,"],
                "records_telephone":record["records_telephone,"],
                "records_telephone_2":record["records_telephone_2,"],
                "records_has_art_unique_code":record["records_has_art_unique_code,"],
                "records_art_unique_code":record["records_art_unique_code,"],
                "records_status":record["records_status,"],
                "records_ward_bed_number":record["records_ward_bed_number,"],
                "records_currently_pregnant":record["records_currently_pregnant,"],
                "records_symptoms_current_cough":record["records_symptoms_current_cough,"],
                "records_symptoms_fever":record["records_symptoms_fever,"],
                "records_symptoms_night_sweats":record["records_symptoms_night_sweats,"],
                "records_symptoms_weight_loss":record["records_symptoms_weight_loss,"],
                "records_symptoms_none_of_the_above":record["records_symptoms_none_of_the_above,"],
                "records_patient_category_hospitalized":record["records_patient_category_hospitalized,"],
                "records_patient_category_child":record["records_patient_category_child,"],
                "records_patient_category_to_initiate_art":record["records_patient_category_to_initiate_art,"],
                "records_patient_category_on_art_symptomatic":record["records_patient_category_on_art_symptomatic,"],
                "records_patient_category_outpatient":record["records_patient_category_outpatient,"],
                "records_patient_category_anc":record["records_patient_category_anc,"],
                "records_patient_category_diabetes_clinic":record["records_patient_category_diabetes_clinic,"],
                "records_patient_category_other":record["records_patient_category_other,"],
                "records_reason_for_test_presumptive_tb":record["records_reason_for_test_presumptive_tb,"],
                "records_tb_treatment_history":record["records_tb_treatment_history,"],
                "records_tb_treatment_history_contact_of_tb_patient":record["records_tb_treatment_history_contact_of_tb_patient"]
            })

        logger.info("Successfully fetched all records")
        return result
    except DatabaseError as err:
        logger.error(f"failed to fetch all records check logs")
        raise InternalServerError(err)
