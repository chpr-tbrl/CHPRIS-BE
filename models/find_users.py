import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def find_user(user_id: int) -> dict:
    """
    Find a user.

    Arguments:
        user_id: int
    
    Returns:
        dict
    """
    try:
        logger.debug("finding user %d ..." % user_id)
        
        users = (
            Users.select()
            .where(Users.id == user_id, Users.state == "verified")
            .dicts()
        )

        result = []
        for user in users:
            result.append(user)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple users %d found" % user_id)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No user found")
            raise Unauthorized()

        logger.info("- User %d found" % user_id)

        return result[0]

    except DatabaseError as err:
        logger.error("failed to find user %d check logs" % user_id)
        raise InternalServerError(err) from None
