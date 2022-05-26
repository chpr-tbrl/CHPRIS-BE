import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.follow_up import Follow_ups

from werkzeug.exceptions import InternalServerError

def find_follow_up(follow_up_records_id: int) -> list:
    """
    """
    try:
        logger.debug("finding lab records for %s ..." % follow_up_records_id)
        result = []
        
        follow_ups = (
            Follow_ups.select()
            .where(Follow_ups.follow_up_records_id == follow_up_records_id)
            .dicts()
        )
        for follow_up in follow_ups:
            result.append(follow_up)

        logger.info("- Successfully found follow_up records for %s" % follow_up_records_id)
        return result

    except DatabaseError as err:
        logger.error("failed to finding follow_ups record for %s check logs" % follow_up_records_id)
        raise InternalServerError(err) from None
