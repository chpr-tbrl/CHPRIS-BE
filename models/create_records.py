import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError
from peewee import OperationalError

from schemas.records.records import Records

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_record(site_id: int, region_id: int, records_user_id: int, records_name: str, records_age: int, records_sex: str, records_date_of_test_request: str, records_address: str, records_telephone: str, records_telephone_2: str, records_has_art_unique_code: str, records_art_unique_code: str, records_status: str, records_ward_bed_number: str, records_currently_pregnant: str, records_symptoms_current_cough: str, records_symptoms_fever: bool, records_symptoms_night_sweats: bool, records_symptoms_weight_loss: bool, records_symptoms_none_of_the_above: bool, records_patient_category_hospitalized: bool, records_patient_category_child: bool, records_patient_category_to_initiate_art: bool, records_patient_category_on_art_symptomatic: bool, records_patient_category_outpatient: bool, records_patient_category_anc: bool, records_patient_category_diabetes_clinic: bool, records_patient_category_other: str, records_reason_for_test_presumptive_tb: bool, records_tb_treatment_history: str, records_tb_treatment_history_contact_of_tb_patient: str) -> str:
    """
    Create a new record.

    Arguments::
        site_id: int,
        region_id: int, 
        records_user_id: int,
        records_name: str,
        records_age: int,
        records_sex: str,
        records_date_of_test_request: str,
        records_address: str,
        records_telephone: str,
        records_telephone_2: str,
        records_has_art_unique_code: str,
        records_art_unique_code: str,
        records_status: str,
        records_ward_bed_number: str,
        records_currently_pregnant: str,
        records_symptoms_current_cough: str,
        records_symptoms_fever: bool,
        records_symptoms_night_sweats: bool,
        records_symptoms_weight_loss: bool,
        records_symptoms_none_of_the_above: bool,
        records_patient_category_hospitalized: bool,
        records_patient_category_child: bool,
        records_patient_category_to_initiate_art: bool,
        records_patient_category_on_art_symptomatic: bool,
        records_patient_category_outpatient: bool,
        records_patient_category_anc: bool,
        records_patient_category_diabetes_clinic: bool,
        records_patient_category_other: str,
        records_reason_for_test_presumptive_tb: bool,
        records_tb_treatment_history: str,
        records_tb_treatment_history_contact_of_tb_patient: str
    
    Returns:
        str
    """
    try:
        logger.debug("creating record for %d ..." % records_user_id)
        
        data = Data()
        record = Records.create(
            site_id=site_id,
            region_id=region_id,
            records_user_id=records_user_id,
            records_name= data.encrypt(records_name),
            records_age=records_age,
            records_sex=records_sex,
            records_date_of_test_request=records_date_of_test_request,
            records_address= data.encrypt(records_address),
            records_telephone= data.encrypt(records_telephone),
            records_telephone_2= data.encrypt(records_telephone_2),
            records_has_art_unique_code=records_has_art_unique_code,
            records_art_unique_code= data.encrypt(records_art_unique_code),
            records_status=records_status,
            records_ward_bed_number= data.encrypt(records_ward_bed_number),
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
            records_tb_treatment_history_contact_of_tb_patient= data.encrypt(records_tb_treatment_history_contact_of_tb_patient),
            iv = data.iv
        )

        logger.info("- Record %s successfully created" % record)
        return str(record)

    except OperationalError as error:
        logger.error(error)
        raise BadRequest()

    except DatabaseError as err:
        logger.error("creating record %d failed check logs" % records_user_id)
        raise InternalServerError(err) from None
