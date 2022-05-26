import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.outcome_recorded import Outcome_recorded

from werkzeug.exceptions import InternalServerError

def find_outcome_recorded(outcome_recorded_records_id: int) -> list:
    """
    """
    try:
        logger.debug("finding outcome_recorded records for %s ..." % outcome_recorded_records_id)
        result = []
        
        outcomes_recorded = (
            Outcome_recorded.select()
            .where(Outcome_recorded.outcome_recorded_records_id == outcome_recorded_records_id)
            .dicts()
        )
        for outcome_recorded in outcomes_recorded:
            result.append(outcome_recorded)

        logger.info("- Successfully found outcome_recorded records for %s" % outcome_recorded_records_id)
        return result
        
    except DatabaseError as err:
        logger.error("failed to finding outcome_recorded record for %s check logs" % outcome_recorded_records_id)
        raise InternalServerError(err) from None
