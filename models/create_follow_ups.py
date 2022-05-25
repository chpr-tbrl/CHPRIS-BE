import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.follow_up import Follow_ups

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_follow_up(follow_up_records_id: int, follow_up_user_id: int, follow_up_xray: str, follow_up_amoxicillin: str, follow_up_other_antibiotic: str, follow_up_schedule_date: str, follow_up_comments: str) -> str:
    """
    """
    try:
        logger.debug("creating follow_up record for %s ..." % follow_up_user_id)

        follow_up = Follow_ups.create(
            follow_up_records_id=follow_up_records_id,
            follow_up_user_id=follow_up_user_id,
            follow_up_xray=follow_up_xray,
            follow_up_amoxicillin=follow_up_amoxicillin,
            follow_up_other_antibiotic=follow_up_other_antibiotic,
            follow_up_schedule_date=follow_up_schedule_date,
            follow_up_comments=follow_up_comments
        )

        logger.info("Follow_up record %s successfully created" % follow_up)
        return str(follow_up)

    except OperationalError as error:
        logger.error(error)
        raise BadRequest()

    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()

    except DatabaseError as err:
        logger.error("creating Follow_up record %s failed check logs" % follow_up)
        raise InternalServerError(err) from None
