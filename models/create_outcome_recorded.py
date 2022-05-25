import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.outcome_recorded import Outcome_recorded

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_outcome_recorded(outcome_recorded_records_id: int, outcome_recorded_user_id: int, outcome_recorded_started_tb_treatment_outcome: str, outcome_recorded_tb_rx_number: str, outcome_recorded_other: str, outcome_recorded_comments: str) -> str:
    """
    """
    try:
        logger.debug("creating outcome_recorded record for %s ..." % outcome_recorded_user_id)

        outcome_recorded = Outcome_recorded.create(
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
