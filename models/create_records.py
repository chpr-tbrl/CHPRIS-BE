import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError
from schemas.records.records import Records

logger = logging.getLogger(__name__)

def create_record(
    site_id,
    region_id,
    records_user_id,
    records_name,
    records_age,
    records_sex,
    records_date_of_test_request,
    records_address,
    records_telephone,
    records_telephone_2,
    records_has_art_unique_code,
    records_art_unique_code,
    records_status,
    records_ward_bed_number,
    records_currently_pregnant,
    records_symptoms_current_cough,
    records_symptoms_fever,
    records_symptoms_night_sweats,
    records_symptoms_weight_loss,
    records_symptoms_none_of_the_above,
    records_patient_category_hospitalized,
    records_patient_category_child,
    records_patient_category_to_initiate_art,
    records_patient_category_on_art_symptomatic,
    records_patient_category_outpatient,
    records_patient_category_anc,
    records_patient_category_diabetes_clinic,
    records_patient_category_other,
    records_reason_for_test_presumptive_tb,
    records_tb_treatment_history,
    records_tb_treatment_history_contact_of_tb_patient
    ):
    try:
        logger.debug(f"creating record for {records_user_id} ...")

        if not records_sex in ["male", "female"]:
            logger.error(f"records_sex got invalid value {records_sex}")
            raise BadRequest()
        if not records_has_art_unique_code in ["yes", "no", "unknown"]:
            logger.error(f"records_has_art_unique_code got invalid value {records_has_art_unique_code}")
            raise BadRequest()
        if not records_status in ["outpatient", "ward-bed"]:
            logger.error(f"records_status got invalid value {records_status}")
            raise BadRequest()
        if not records_currently_pregnant in ["yes", "no"]:
            logger.error(f"records_currently_pregnant got invalid value {records_currently_pregnant}")
            raise BadRequest()
        if not records_tb_treatment_history in ["new", "relapse", "after_loss_to_follow_up", "failure"]:
            logger.error(f"records_tb_treatment_history got invalid value {records_tb_treatment_history}")
            raise BadRequest()
        
        record = Records.create(
            site_id=site_id,
            region_id=region_id,
            records_user_id=records_user_id,
            records_name=records_name,
            records_age=records_age,
            records_sex=records_sex,
            records_date_of_test_request=records_date_of_test_request,
            records_address=records_address,
            records_telephone=records_telephone,
            records_telephone_2=records_telephone_2,
            records_has_art_unique_code=records_has_art_unique_code,
            records_art_unique_code=records_art_unique_code,
            records_status=records_status,
            records_ward_bed_number=records_ward_bed_number,
            records_currently_pregnant=records_currently_pregnant,
            records_symptoms_current_cough=records_symptoms_current_cough,
            records_symptoms_fever=records_symptoms_fever,
            records_symptoms_night_sweats=records_symptoms_night_sweats,
            records_symptoms_weight_loss=records_symptoms_weight_loss,
            records_symptoms_none_of_the_above=records_symptoms_none_of_the_above,
            records_patient_category_hospitalized=records_patient_category_hospitalized,
            records_patient_category_child=records_patient_category_child,
            records_patient_category_to_initiate_art=records_patient_category_to_initiate_art,
            records_patient_category_on_art_symptomatic=records_patient_category_on_art_symptomatic,
            records_patient_category_outpatient=records_patient_category_outpatient,
            records_patient_category_anc=records_patient_category_anc,
            records_patient_category_diabetes_clinic=records_patient_category_diabetes_clinic,
            records_patient_category_other=records_patient_category_other,
            records_reason_for_test_presumptive_tb=records_reason_for_test_presumptive_tb,
            records_tb_treatment_history=records_tb_treatment_history,
            records_tb_treatment_history_contact_of_tb_patient=records_tb_treatment_history_contact_of_tb_patient
        )

        logger.info(f"Record {record} successfully created")
        return str(record)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating record {records_user_id} failed check logs")
        raise InternalServerError(err)
