import logging
logger = logging.getLogger(__name__)

from error import InternalServerError

from peewee import DatabaseError
from schemas.records.lab import Labs

def find_lab(lab_user_id, lab_records_id):
    """
    """
    try:
        logger.debug(f"finding lab records for {lab_user_id} ...")
        result = []
        
        labs = (
            Labs.select()
            .where(Labs.lab_user_id == lab_user_id, Labs.lab_records_id == lab_records_id)
            .dicts()
        )
        for lab in labs:
            result.append(lab)

        logger.info(f"Successfully found lab records for {lab_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding lab record for {lab_user_id} check logs")
        raise InternalServerError(err)
