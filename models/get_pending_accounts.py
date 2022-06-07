from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import InternalServerError

def get_pending_account() -> list:
    """
    """
    try:
        logger.debug("Fetching all pending accounts ...")  
           
        pending_users = (
            Users.select()
            .where(Users.account_status == "pending")
            .dicts()
        )

        result = []

        for user in pending_users.iterator():
            result.append(user)

        logger.info("- Successfully fetched all pending accounts")

        return result

    except DatabaseError as err:
        logger.error("Failed to fetch pending accounts check logs")
        raise InternalServerError(err) from None
