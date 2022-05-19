import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError, IntegrityError
from schemas.records.outcome_recorded import Outcome_recorded

logger = logging.getLogger(__name__)

def create_outcome_recorded(
    outcome_recorded_records_id,
    outcome_recorded_user_id,
    outcome_recorded_started_tb_treatment_outcome,
    outcome_recorded_tb_rx_number,
    outcome_recorded_other,
    outcome_recorded_comments
    ):
    try:
        logger.debug(f"creating outcome_recorded record for {outcome_recorded_user_id} ...")

        if not outcome_recorded_started_tb_treatment_outcome in ["started_tb_treatment", "referred_for_treatment", "other"]:
            logger.error(f"outcome_recorded_started_tb_treatment_outcome got invalid value '{outcome_recorded_started_tb_treatment_outcome}'")
            raise BadRequest()

        outcome_recorded = Outcome_recorded.create(
            outcome_recorded_records_id=outcome_recorded_records_id,
            outcome_recorded_user_id=outcome_recorded_user_id,
            outcome_recorded_started_tb_treatment_outcome=outcome_recorded_started_tb_treatment_outcome,
            outcome_recorded_tb_rx_number=outcome_recorded_tb_rx_number,
            outcome_recorded_other=outcome_recorded_other,
            outcome_recorded_comments=outcome_recorded_comments
        )

        logger.info(f"Outcome_recorded record {outcome_recorded} successfully created")
        return str(outcome_recorded)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating outcome_recorded record {outcome_recorded} failed check logs")
        raise InternalServerError(err)
