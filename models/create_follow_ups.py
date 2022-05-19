import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError, IntegrityError
from schemas.records.follow_up import Follow_ups

logger = logging.getLogger(__name__)

def create_follow_up(
    follow_up_records_id,
    follow_up_user_id,
    follow_up_xray, 
    follow_up_amoxicillin, 
    follow_up_other_antibiotic, 
    follow_up_schedule_date, 
    follow_up_comments 
    ):
    try:
        logger.debug(f"creating follow_up record for {follow_up_user_id} ...")

        follow_up = Follow_ups.create(
            follow_up_records_id=follow_up_records_id,
            follow_up_user_id=follow_up_user_id,
            follow_up_xray=follow_up_xray,
            follow_up_amoxicillin=follow_up_amoxicillin,
            follow_up_other_antibiotic=follow_up_other_antibiotic,
            follow_up_schedule_date=follow_up_schedule_date,
            follow_up_comments=follow_up_comments
        )

        logger.info(f"Follow_up record {follow_up} successfully created")
        return str(follow_up)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating Follow_up record {follow_up} failed check logs")
        raise InternalServerError(err)
