import logging
logger = logging.getLogger(__name__)

from error import Conflict, InternalServerError, Unauthorized

from peewee import DatabaseError
from schemas.users.users import Users

def change_state(user_id: int, state: str) -> bool:
    """
    """
    try:
        logger.debug("Verifying state %s ..." % state)

        if not state in ["pending", "verified", "suspended"]:
            logger.error("invalid state '%s'" % state)
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

        logger.debug("updating state %s for user %s ..." % (state, user_id))
        upd_state = Users.update(state=state).where(
            Users.id == user_id
        )
        upd_state.execute()

        logger.info("- SUCCESSFULLY UPDATED STATE FOR %s" % user_id)
        return True
    except DatabaseError as err:
        logger.error("FAILED UPDATING STATE FOR USER %s CHECK LOGS" % user_id)
        raise InternalServerError(err)
