import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.tb_treatment_outcome import Tb_treatment_outcomes

logger = logging.getLogger(__name__)

def find_tb_treatment_outcome(tb_treatment_outcome_user_id, tb_treatment_outcome_records_id):
    try:
        logger.debug(f"finding tb_treatment_outcome records for {tb_treatment_outcome_user_id} ...")
        result = []
        
        tb_treatment_outcomes = (
            Tb_treatment_outcomes.select()
            .where(Tb_treatment_outcomes.tb_treatment_outcome_user_id == tb_treatment_outcome_user_id, Tb_treatment_outcomes.tb_treatment_outcome_records_id == tb_treatment_outcome_records_id)
            .dicts()
        )
        for tb_treatment_outcome in tb_treatment_outcomes:
            result.append(tb_treatment_outcome)

        logger.info(f"Successfully found tb_treatment_outcome records for {tb_treatment_outcome_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding tb_treatment_outcome record for {tb_treatment_outcome_user_id} check logs")
        raise InternalServerError(err)
