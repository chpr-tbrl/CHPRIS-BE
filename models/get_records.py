import logging
logger = logging.getLogger(__name__)

from error import InternalServerError

from peewee import DatabaseError
from schemas.records.records import Records

def get_all_records():
    """
    """
    try:
        logger.debug("fetching all records ...")
        result = []
        
        records = (
            Records.select()
            .dicts()
        )
        for record in records:
            result.append(record)

        logger.info("- Successfully fetched all records")
        return result
    except DatabaseError as err:
        logger.error("failed to fetch all records check logs")
        raise InternalServerError(err)
