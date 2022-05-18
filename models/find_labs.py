import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.lab import Lab

logger = logging.getLogger(__name__)

def find_lab(lab_user_id, lab_records_id):
    try:
        logger.debug(f"finding lab records for {lab_user_id} ...")
        result = []
        
        labs = (
            Lab.select()
            .where(Lab.lab_user_id == lab_user_id, Lab.lab_records_id == lab_records_id)
            .dicts()
        )
        for lab in labs:
            result.append(lab)

        logger.info(f"Successfully found lab records for {lab_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding lab record for {lab_user_id} check logs")
        raise InternalServerError(err)
