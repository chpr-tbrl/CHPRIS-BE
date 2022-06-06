from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import InternalServerError

def update_account_status(user_id: int, account_status: str) -> bool:
    """
    """
    try:
        logger.debug("Verifying account_status %s ..." % account_status)

        if not account_status in ["pending", "approved", "suspended"]:
            logger.error("invalid account_status '%s'" % account_status)
            raise Unauthorized()        
           
        logger.debug("finding user %s ..." % user_id)
        users = (
            Users.select()
            .where(Users.id == user_id)
            .dicts()
        )
        result = []
        for user in users:
            result.append(user)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple users %s found" % user_id)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No user %s found" % user_id)
            raise Unauthorized()

        logger.debug("updating account_status %s for user %s ..." % (account_status, user_id))

        if account_status == "approved":
            upd_account_status = Users.update(account_status=account_status, account_approved_date=datetime.now()).where(
                Users.id == user_id
            )
        else:
            upd_account_status = Users.update(account_status=account_status).where(
                Users.id == user_id
            )
        
        upd_account_status.execute()

        logger.info("- Successfully updated_account_status for user %s" % user_id)
        return True
    except DatabaseError as err:
        logger.error("Failed to updated_account_status for user %s check logs" % user_id)
        raise InternalServerError(err)
