import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.outcome_recorded import Outcome_recorded

logger = logging.getLogger(__name__)

def find_outcome_recorded(outcome_recorded_user_id, outcome_recorded_records_id):
    try:
        logger.debug(f"finding outcome_recorded records for {outcome_recorded_user_id} ...")
        result = []
        
        outcomes_recorded = (
            Outcome_recorded.select()
            .where(Outcome_recorded.outcome_recorded_user_id == outcome_recorded_user_id, Outcome_recorded.outcome_recorded_records_id == outcome_recorded_records_id)
            .dicts()
        )
        for outcome_recorded in outcomes_recorded:
            result.append(outcome_recorded)

        logger.info(f"Successfully found outcome_recorded records for {outcome_recorded_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding outcome_recorded record for {outcome_recorded_user_id} check logs")
        raise InternalServerError(err)
