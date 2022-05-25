import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

from datetime import date

from werkzeug.exceptions import InternalServerError

def find_tb_treatment_outcome(tb_treatment_outcome_records_id: int) -> list:
    """
    """
    try:
        logger.debug("finding tb_treatment_outcome records for %s ..." % tb_treatment_outcome_records_id)
        result = []
        
        tb_treatment_outcomes = (
            Tb_treatment_outcomes.select()
            .where(Tb_treatment_outcomes.tb_treatment_outcome_records_id == tb_treatment_outcome_records_id, Tb_treatment_outcomes.tb_treatment_outcome_date >= date.today())
            .dicts()
        )
        for tb_treatment_outcome in tb_treatment_outcomes:
            result.append(tb_treatment_outcome)

        logger.info("- Successfully found tb_treatment_outcome records for %s" % tb_treatment_outcome_records_id)
        return result
        
    except DatabaseError as err:
        logger.error("failed to finding tb_treatment_outcome record for %s check logs" % tb_treatment_outcome_records_id)
        raise InternalServerError(err) from None
