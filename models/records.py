import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.records import Records
from schemas.records.specimen_collection import Specimen_collections
from schemas.records.lab import Labs
from schemas.records.follow_up import Follow_ups
from schemas.records.outcome_recorded import Outcome_recorded
from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

from datetime import date

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import BadRequest

class Record_Model:
    """
    """
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

    def create_record(self, site_id: int, region_id: int, records_user_id: int, records_name: str, records_age: int, records_sex: str, records_date_of_test_request: str, records_address: str, records_telephone: str, records_telephone_2: str, records_has_art_unique_code: str, records_art_unique_code: str, records_status: str, records_ward_bed_number: str, records_currently_pregnant: str, records_symptoms_current_cough: str, records_symptoms_fever: bool, records_symptoms_night_sweats: bool, records_symptoms_weight_loss: bool, records_symptoms_none_of_the_above: bool, records_patient_category_hospitalized: bool, records_patient_category_child: bool, records_patient_category_to_initiate_art: bool, records_patient_category_on_art_symptomatic: bool, records_patient_category_outpatient: bool, records_patient_category_anc: bool, records_patient_category_diabetes_clinic: bool, records_patient_category_other: str, records_reason_for_test_presumptive_tb: bool, records_tb_treatment_history: str, records_tb_treatment_history_contact_of_tb_patient: str) -> str:
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
            
            data = self.Data()

            record = Records.create(
                site_id=site_id,
                region_id=region_id,
                records_user_id=records_user_id,
                records_name= data.encrypt(records_name)["e_data"],
                records_age=records_age,
                records_sex=records_sex,
                records_date_of_test_request=records_date_of_test_request,
                records_address= data.encrypt(records_address)["e_data"],
                records_telephone= data.encrypt(records_telephone)["e_data"],
                records_telephone_2= data.encrypt(records_telephone_2)["e_data"],
                records_has_art_unique_code=records_has_art_unique_code,
                records_art_unique_code= data.encrypt(records_art_unique_code)["e_data"],
                records_status=records_status,
                records_ward_bed_number= data.encrypt(records_ward_bed_number)["e_data"],
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
                records_tb_treatment_history_contact_of_tb_patient= data.encrypt(records_tb_treatment_history_contact_of_tb_patient)["e_data"],
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

    def fetch_record(self, site_id: int, region_id: int, records_user_id: int, permitted_decrypted_data: bool) -> list:
        """
        Fetch all records >= today by site_id and region_id.

        Arguments:
            site_id: int,
            region_id: int,
            records_user_id: int,
            permitted_decrypted_data; bool

        Returns:
            list
        """
        try:
            logger.debug("finding records for %d ..." % records_user_id)

            result = []
            
            records = (
                self.Records.select(
                    self.Records.record_id,
                    self.Records.records_name,
                    self.Records.records_date,
                    self.Records.records_sex,
                    self.Records.records_date_of_test_request,
                    self.Records.iv
                ).where(
                    self.Records.site_id == site_id,
                    self.Records.region_id == region_id,
                    self.Records.records_date >= date.today()
                ).dicts()
            )

            for record in records.iterator():
                if permitted_decrypted_data:
                    iv = record["iv"]

                    data = self.Data()

                    result.append({
                        "record_id" : record["record_id"],
                        "records_name" : data.decrypt(record["records_name"], iv),
                        "records_date" : record["records_date"],
                        "records_sex" : record["records_sex"],
                        "records_date_of_test_request" : record["records_date_of_test_request"]
                    })
                else:
                    result.append({
                        "record_id" : record["record_id"],
                        "records_name" : record["records_name"],
                        "records_date" : record["records_date"],
                        "records_sex" : record["records_sex"],
                        "records_date_of_test_request" : record["records_date_of_test_request"]
                    })

            logger.info("- Successfully found records with site_id = %s & region_id = %s requested by user_id = %s" % (site_id, region_id, records_user_id))
            return result

        except DatabaseError as err:
            logger.error("failed to find record for %d check logs" % records_user_id)
            raise InternalServerError(err) from None

    def fetch_records(self, permitted_decrypted_data: bool) -> list:
        """
        Fetch all records.

        Arguments:
            permitted_decrypted_data: bool

        Returns:
            list
        """
        try:
            logger.debug("fetching all records ...")

            result = []

            data = self.Data()

            records = (
                self.Records.select()
                .dicts()
            )

            for record in records.iterator():
                result.append(record)

            if permitted_decrypted_data:
                iv = record["iv"]

                data = self.Data()
                
                result.append({
                    'record_id':record['record_id'],
                    'site_id':record['site_id'],
                    'region_id':record['region_id'],
                    'records_user_id':record['records_user_id'],
                    'records_date':record['records_date'],
                    'records_name': data.decrypt(record['records_name'], iv),
                    'records_age':record['records_age'],
                    'records_sex':record['records_sex'],
                    'records_date_of_test_request':record['records_date_of_test_request'],
                    'records_address': data.decrypt(record['records_address'], iv),
                    'records_telephone': data.decrypt(record['records_telephone'], iv),
                    'records_telephone_2': data.decrypt(record['records_telephone_2'], iv),
                    'records_has_art_unique_code':record['records_has_art_unique_code'],
                    'records_art_unique_code': data.decrypt(record['records_art_unique_code'], iv),
                    'records_status':record['records_status'],
                    'records_ward_bed_number': data.decrypt(record['records_ward_bed_number'], iv),
                    'records_currently_pregnant':record['records_currently_pregnant'],
                    'records_symptoms_current_cough':record['records_symptoms_current_cough'],
                    'records_symptoms_fever':record['records_symptoms_fever'],
                    'records_symptoms_night_sweats':record['records_symptoms_night_sweats'],
                    'records_symptoms_weight_loss':record['records_symptoms_weight_loss'],
                    'records_symptoms_none_of_the_above':record['records_symptoms_none_of_the_above'],
                    'records_patient_category_hospitalized':record['records_patient_category_hospitalized'],
                    'records_patient_category_child':record['records_patient_category_child'],
                    'records_patient_category_to_initiate_art':record['records_patient_category_to_initiate_art'],
                    'records_patient_category_on_art_symptomatic':record['records_patient_category_on_art_symptomatic'],
                    'records_patient_category_outpatient':record['records_patient_category_outpatient'],
                    'records_patient_category_anc':record['records_patient_category_anc'],
                    'records_patient_category_diabetes_clinic':record['records_patient_category_diabetes_clinic'],
                    'records_patient_category_other':record['records_patient_category_other'],
                    'records_reason_for_test_presumptive_tb':record['records_reason_for_test_presumptive_tb'],
                    'records_tb_treatment_history':record['records_tb_treatment_history'],
                    'records_tb_treatment_history_contact_of_tb_patient': data.decrypt(record['records_tb_treatment_history_contact_of_tb_patient'], iv)
                })
            else:
                result.append({
                    'record_id':record['record_id'],
                    'site_id':record['site_id'],
                    'region_id':record['region_id'],
                    'records_user_id':record['records_user_id'],
                    'records_date':record['records_date'],
                    'records_name':record['records_name'],
                    'records_age':record['records_age'],
                    'records_sex':record['records_sex'],
                    'records_date_of_test_request':record['records_date_of_test_request'],
                    'records_address':record['records_address'],
                    'records_telephone':record['records_telephone'],
                    'records_telephone_2':record['records_telephone_2'],
                    'records_has_art_unique_code':record['records_has_art_unique_code'],
                    'records_art_unique_code':record['records_art_unique_code'],
                    'records_status':record['records_status'],
                    'records_ward_bed_number':record['records_ward_bed_number'],
                    'records_currently_pregnant':record['records_currently_pregnant'],
                    'records_symptoms_current_cough':record['records_symptoms_current_cough'],
                    'records_symptoms_fever':record['records_symptoms_fever'],
                    'records_symptoms_night_sweats':record['records_symptoms_night_sweats'],
                    'records_symptoms_weight_loss':record['records_symptoms_weight_loss'],
                    'records_symptoms_none_of_the_above':record['records_symptoms_none_of_the_above'],
                    'records_patient_category_hospitalized':record['records_patient_category_hospitalized'],
                    'records_patient_category_child':record['records_patient_category_child'],
                    'records_patient_category_to_initiate_art':record['records_patient_category_to_initiate_art'],
                    'records_patient_category_on_art_symptomatic':record['records_patient_category_on_art_symptomatic'],
                    'records_patient_category_outpatient':record['records_patient_category_outpatient'],
                    'records_patient_category_anc':record['records_patient_category_anc'],
                    'records_patient_category_diabetes_clinic':record['records_patient_category_diabetes_clinic'],
                    'records_patient_category_other':record['records_patient_category_other'],
                    'records_reason_for_test_presumptive_tb':record['records_reason_for_test_presumptive_tb'],
                    'records_tb_treatment_history':record['records_tb_treatment_history'],
                    'records_tb_treatment_history_contact_of_tb_patient':record['records_tb_treatment_history_contact_of_tb_patient']
                })

            logger.info("- Successfully fetched all records")
            return result

        except DatabaseError as err:
            logger.error("failed to fetch all records check logs")
            raise InternalServerError(err) from None

    def create_specimen_collection(self, specimen_collection_records_id: int, specimen_collection_user_id: int, specimen_collection_1_date: str, specimen_collection_1_specimen_collection_type: str, specimen_collection_1_other: str, specimen_collection_1_period: str, specimen_collection_1_aspect: str, specimen_collection_1_received_by: str, specimen_collection_2_date: str, specimen_collection_2_specimen_collection_type: str, specimen_collection_2_other: str, specimen_collection_2_period: str, specimen_collection_2_aspect: str, specimen_collection_2_received_by: str) -> str:
        """
        Create a new specimen_collections record.

        Arguments:
            specimen_collection_records_id: int,
            specimen_collection_user_id: int,
            specimen_collection_1_date: str,
            specimen_collection_1_specimen_collection_type: str,
            specimen_collection_1_other: str,
            specimen_collection_1_period: str,
            specimen_collection_1_aspect: str,
            specimen_collection_1_received_by: str,
            specimen_collection_2_date: str,
            specimen_collection_2_specimen_collection_type: str,
            specimen_collection_2_other: str,
            specimen_collection_2_period: str,
            specimen_collection_2_aspect: str,
            specimen_collection_2_received_by: str
                
        Returns:
            str
        """
        try:
            logger.debug("creating specimen_collection record for %s ..." % specimen_collection_user_id)
            
            specimen_collection = self.Specimen_collections.create(
                specimen_collection_records_id=specimen_collection_records_id,
                specimen_collection_user_id=specimen_collection_user_id,
                specimen_collection_1_date=specimen_collection_1_date,
                specimen_collection_1_specimen_collection_type=specimen_collection_1_specimen_collection_type,
                specimen_collection_1_other=specimen_collection_1_other,
                specimen_collection_1_period=specimen_collection_1_period,
                specimen_collection_1_aspect=specimen_collection_1_aspect,
                specimen_collection_1_received_by=specimen_collection_1_received_by,
                specimen_collection_2_date=specimen_collection_2_date,
                specimen_collection_2_specimen_collection_type=specimen_collection_2_specimen_collection_type,
                specimen_collection_2_other=specimen_collection_2_other,
                specimen_collection_2_period=specimen_collection_2_period,
                specimen_collection_2_aspect=specimen_collection_2_aspect,
                specimen_collection_2_received_by=specimen_collection_2_received_by
            )

            logger.info("- Specimen_collection record %s successfully created" % specimen_collection)
            return str(specimen_collection)

        except OperationalError as error:
            logger.error(error)
            raise BadRequest()

        except IntegrityError as error:
            logger.error(error)
            raise BadRequest()
            
        except DatabaseError as err:
            logger.error("creating Specimen_collection record failed check logs")
            raise InternalServerError(err) from None

    def fetch_specimen_collection(self, specimen_collection_records_id: int) -> list:
        """
        Fetch specimen_collection records >= today by record_id.

        Arguments:
            specimen_collection_records_id: int

        Returns:
            list
        """
        try:
            logger.debug("finding specimen_collection records for %d ..." % specimen_collection_records_id)

            result = []
            
            specimen_collections = (
                self.Specimen_collections.select()
                .where(self.Specimen_collections.specimen_collection_records_id == specimen_collection_records_id)
                .dicts()
            )

            for specimen_collection in specimen_collections:
                result.append(specimen_collection)

            logger.info("- Successfully found specimen_collection records for %d" % specimen_collection_records_id)
            return result

        except DatabaseError as err:
            logger.error("failed to find specimen_collection record for %d check logs" % specimen_collection_records_id)
            raise InternalServerError(err) from None

    def create_lab(self, lab_records_id: int, lab_user_id: int, lab_date_specimen_collection_received: str, lab_received_by: str, lab_registration_number: str, lab_smear_microscopy_result_result_1: str, lab_smear_microscopy_result_result_2: str, lab_smear_microscopy_result_date: str, lab_smear_microscopy_result_done_by: str, lab_xpert_mtb_rif_assay_result: str, lab_xpert_mtb_rif_assay_grades: str, lab_xpert_mtb_rif_assay_rif_result: str, lab_xpert_mtb_rif_assay_date: str, lab_xpert_mtb_rif_assay_done_by: str, lab_urine_lf_lam_result: str, lab_urine_lf_lam_date: str, lab_urine_lf_lam_done_by: str) -> str:
        """
        """
        try:
            logger.debug("creating lab record for %d ..." % lab_user_id)
            
            lab = self.Labs.create(
                lab_records_id=lab_records_id,
                lab_user_id=lab_user_id,
                lab_date_specimen_collection_received=lab_date_specimen_collection_received,
                lab_received_by=lab_received_by,
                lab_registration_number=lab_registration_number,
                lab_smear_microscopy_result_result_1=lab_smear_microscopy_result_result_1,
                lab_smear_microscopy_result_result_2=lab_smear_microscopy_result_result_2,
                lab_smear_microscopy_result_date=lab_smear_microscopy_result_date,
                lab_smear_microscopy_result_done_by=lab_smear_microscopy_result_done_by,
                lab_xpert_mtb_rif_assay_result=lab_xpert_mtb_rif_assay_result,
                lab_xpert_mtb_rif_assay_grades=lab_xpert_mtb_rif_assay_grades,
                lab_xpert_mtb_rif_assay_rif_result=lab_xpert_mtb_rif_assay_rif_result,
                lab_xpert_mtb_rif_assay_date=lab_xpert_mtb_rif_assay_date,
                lab_xpert_mtb_rif_assay_done_by=lab_xpert_mtb_rif_assay_done_by,
                lab_urine_lf_lam_result=lab_urine_lf_lam_result,
                lab_urine_lf_lam_date=lab_urine_lf_lam_date,
                lab_urine_lf_lam_done_by=lab_urine_lf_lam_done_by
            )

            logger.info("- Lab record %s successfully created" % lab)
            return str(lab)

        except OperationalError as error:
            logger.error(error)
            raise BadRequest()

        except IntegrityError as error:
            logger.error(error)
            raise BadRequest()

        except DatabaseError as err:
            logger.error("creating Lab record %s failed check logs" % lab)
            raise InternalServerError(err) from None
            
    def fetch_lab(self, lab_records_id: int) -> list:
        """
        """
        try:
            logger.debug("finding lab records for %d ..." % lab_records_id)

            result = []
            
            labs = (
                self.Labs.select()
                .where(self.Labs.lab_records_id == lab_records_id)
                .dicts()
            )

            for lab in labs:
                result.append(lab)

            logger.info("- Successfully found lab records for %d" % lab_records_id)
            return result

        except DatabaseError as err:
            logger.error("failed to find lab record for %d check logs" % lab_records_id)
            raise InternalServerError(err) from None

    def create_follow_up(self, follow_up_records_id: int, follow_up_user_id: int, follow_up_xray: str, follow_up_amoxicillin: str, follow_up_other_antibiotic: str, follow_up_schedule_date: str, follow_up_comments: str) -> str:
        """
        """
        try:
            logger.debug("creating follow_up record for %s ..." % follow_up_user_id)

            follow_up = self.Follow_ups.create(
                follow_up_records_id=follow_up_records_id,
                follow_up_user_id=follow_up_user_id,
                follow_up_xray=follow_up_xray,
                follow_up_amoxicillin=follow_up_amoxicillin,
                follow_up_other_antibiotic=follow_up_other_antibiotic,
                follow_up_schedule_date=follow_up_schedule_date,
                follow_up_comments=follow_up_comments
            )

            logger.info("Follow_up record %s successfully created" % follow_up)
            return str(follow_up)

        except OperationalError as error:
            logger.error(error)
            raise BadRequest()

        except IntegrityError as error:
            logger.error(error)
            raise BadRequest()

        except DatabaseError as err:
            logger.error("creating Follow_up record %s failed check logs" % follow_up)
            raise InternalServerError(err) from None

    def fetch_follow_up(self, follow_up_records_id: int) -> list:
        """
        """
        try:
            logger.debug("finding lab records for %s ..." % follow_up_records_id)

            result = []
            
            follow_ups = (
                self.Follow_ups.select()
                .where(self.Follow_ups.follow_up_records_id == follow_up_records_id)
                .dicts()
            )

            for follow_up in follow_ups:
                result.append(follow_up)

            logger.info("- Successfully found follow_up records for %s" % follow_up_records_id)
            return result

        except DatabaseError as err:
            logger.error("failed to finding follow_ups record for %s check logs" % follow_up_records_id)
            raise InternalServerError(err) from None

    def create_outcome_recorded(self, outcome_recorded_records_id: int, outcome_recorded_user_id: int, outcome_recorded_started_tb_treatment_outcome: str, outcome_recorded_tb_rx_number: str, outcome_recorded_other: str, outcome_recorded_comments: str) -> str:
        """
        """
        try:
            logger.debug("creating outcome_recorded record for %s ..." % outcome_recorded_user_id)

            outcome_recorded = self.Outcome_recorded.create(
                outcome_recorded_records_id=outcome_recorded_records_id,
                outcome_recorded_user_id=outcome_recorded_user_id,
                outcome_recorded_started_tb_treatment_outcome=outcome_recorded_started_tb_treatment_outcome,
                outcome_recorded_tb_rx_number=outcome_recorded_tb_rx_number,
                outcome_recorded_other=outcome_recorded_other,
                outcome_recorded_comments=outcome_recorded_comments
            )

            logger.info("Outcome_recorded record %s successfully created" % outcome_recorded)
            return str(outcome_recorded)

        except OperationalError as error:
            logger.error(error)
            raise BadRequest()

        except IntegrityError as error:
            logger.error(error)
            raise BadRequest()

        except DatabaseError as err:
            logger.error("creating outcome_recorded record %s failed check logs" % outcome_recorded)
            raise InternalServerError(err) from None

    def fetch_outcome_recorded(self, outcome_recorded_records_id: int) -> list:
        """
        """
        try:
            logger.debug("finding outcome_recorded records for %s ..." % outcome_recorded_records_id)

            result = []
            
            outcomes_recorded = (
                self.Outcome_recorded.select()
                .where(self.Outcome_recorded.outcome_recorded_records_id == outcome_recorded_records_id)
                .dicts()
            )

            for outcome_recorded in outcomes_recorded:
                result.append(outcome_recorded)

            logger.info("- Successfully found outcome_recorded records for %s" % outcome_recorded_records_id)
            return result
            
        except DatabaseError as err:
            logger.error("failed to finding outcome_recorded record for %s check logs" % outcome_recorded_records_id)
            raise InternalServerError(err) from None

    def create_tb_treatment_outcome(self, tb_treatment_outcome_records_id: int, tb_treatment_outcome_user_id: int, tb_treatment_outcome_result: str, tb_treatment_outcome_comments: str, tb_treatment_outcome_close_patient_file: bool) -> str:
        """
        """
        try:
            logger.debug("creating tb_treatment_outcome record for %s ..." % tb_treatment_outcome_user_id)

            tb_treatment_outcome = self.Tb_treatment_outcomes.create(
                tb_treatment_outcome_records_id = tb_treatment_outcome_records_id,
                tb_treatment_outcome_user_id = tb_treatment_outcome_user_id,
                tb_treatment_outcome_result = tb_treatment_outcome_result,
                tb_treatment_outcome_comments = tb_treatment_outcome_comments,
                tb_treatment_outcome_close_patient_file = tb_treatment_outcome_close_patient_file
            )

            logger.info("Tb_treatment_outcome record %s successfully created" % tb_treatment_outcome)
            return str(tb_treatment_outcome)

        except OperationalError as error:
            logger.error(error)
            raise BadRequest()

        except IntegrityError as error:
            logger.error(error)
            raise BadRequest()

        except DatabaseError as err:
            logger.error("creating tb_treatment_outcome record %s failed check logs" % tb_treatment_outcome)
            raise InternalServerError(err) from None

    def fetch_tb_treatment_outcome(self, tb_treatment_outcome_records_id: int) -> list:
        """
        """
        try:
            logger.debug("finding tb_treatment_outcome records for %s ..." % tb_treatment_outcome_records_id)

            result = []
            
            tb_treatment_outcomes = (
                self.Tb_treatment_outcomes.select()
                .where(self.Tb_treatment_outcomes.tb_treatment_outcome_records_id == tb_treatment_outcome_records_id)
                .dicts()
            )

            for tb_treatment_outcome in tb_treatment_outcomes:
                result.append(tb_treatment_outcome)

            logger.info("- Successfully found tb_treatment_outcome records for %s" % tb_treatment_outcome_records_id)
            return result
            
        except DatabaseError as err:
            logger.error("failed to finding tb_treatment_outcome record for %s check logs" % tb_treatment_outcome_records_id)
            raise InternalServerError(err) from None
