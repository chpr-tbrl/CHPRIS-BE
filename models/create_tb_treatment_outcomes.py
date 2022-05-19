import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError, IntegrityError
from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

logger = logging.getLogger(__name__)

def create_tb_treatment_outcome(
    tb_treatment_outcome_records_id,
    tb_treatment_outcome_user_id,
    tb_treatment_outcome_result,
    tb_treatment_outcome_comments,
    tb_treatment_outcome_close_patient_file
    ):
    try:
        logger.debug(f"creating tb_treatment_outcome record for {tb_treatment_outcome_user_id} ...")

        tb_treatment_outcome = Tb_treatment_outcomes.create(
            tb_treatment_outcome_records_id = tb_treatment_outcome_records_id,
            tb_treatment_outcome_user_id = tb_treatment_outcome_user_id,
            tb_treatment_outcome_result = tb_treatment_outcome_result,
            tb_treatment_outcome_comments = tb_treatment_outcome_comments,
            tb_treatment_outcome_close_patient_file = tb_treatment_outcome_close_patient_file
        )

        logger.info(f"Tb_treatment_outcome record {tb_treatment_outcome} successfully created")
        return str(tb_treatment_outcome)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating tb_treatment_outcome record {tb_treatment_outcome} failed check logs")
        raise InternalServerError(err)
