import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.records import Records

from datetime import date

from werkzeug.exceptions import InternalServerError

def find_record(site_id: int, region_id: int, records_user_id: int) -> list:
    """
    Find records >= today by site_id and region_id.

    Arguments:
        site_id: int,
        region_id: int,
        records_user_id: int

    Returns:
        list
    """
    try:
        logger.debug("finding records for %d ..." % records_user_id)
        result = []
        
        records = (
            Records.select()
            .where(Records.site_id == site_id, Records.region_id == region_id, Records.records_date >= date.today())
            .dicts()
        )

        for record in records:
            result.append(record)

        logger.info("- Successfully found records for %d" % records_user_id)
        return result

    except DatabaseError as err:
        logger.error("failed to find record for %d check logs" % records_user_id)
        raise InternalServerError(err) from None
