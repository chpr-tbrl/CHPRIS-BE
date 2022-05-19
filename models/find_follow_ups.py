import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.follow_up import Follow_ups

logger = logging.getLogger(__name__)

def find_follow_up(follow_up_user_id, follow_up_records_id):
    try:
        logger.debug(f"finding lab records for {follow_up_user_id} ...")
        result = []
        
        follow_ups = (
            Follow_ups.select()
            .where(Follow_ups.follow_up_user_id == follow_up_user_id, Follow_ups.follow_up_records_id == follow_up_records_id)
            .dicts()
        )
        for follow_up in follow_ups:
            result.append(follow_up)

        logger.info(f"Successfully found follow_up records for {follow_up_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding follow_ups record for {follow_up_user_id} check logs")
        raise InternalServerError(err)
