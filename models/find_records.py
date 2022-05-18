import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.records import Records

logger = logging.getLogger(__name__)

def find_record(site_id, region_id, records_user_id):
    try:
        logger.debug(f"finding records for {records_user_id} ...")
        result = []
        
        records = (
            Records.select()
            .where(Records.site_id == site_id, Records.region_id == region_id, Records.records_user_id == records_user_id)
            .dicts()
        )
        for record in records:
            result.append(record)

        logger.info(f"Successfully found records for {records_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding record for {records_user_id} check logs")
        raise InternalServerError(err)
