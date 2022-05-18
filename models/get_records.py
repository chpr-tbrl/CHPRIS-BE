import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.records import Records

logger = logging.getLogger(__name__)

def get_all_records():
    try:
        logger.debug(f"fetching all records ...")
        result = []
        
        records = (
            Records.select()
            .dicts()
        )
        for record in records:
            result.append(record)

        logger.info("Successfully fetched all records")
        return result
    except DatabaseError as err:
        logger.error(f"failed to fetch all records check logs")
        raise InternalServerError(err)
