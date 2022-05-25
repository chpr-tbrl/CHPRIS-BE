import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_tb_treatment_outcome(tb_treatment_outcome_records_id: int, tb_treatment_outcome_user_id: int, tb_treatment_outcome_result: str, tb_treatment_outcome_comments: str, tb_treatment_outcome_close_patient_file: bool) -> str:
    """
    """
    try:
        logger.debug("creating tb_treatment_outcome record for %s ..." % tb_treatment_outcome_user_id)

        tb_treatment_outcome = Tb_treatment_outcomes.create(
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
