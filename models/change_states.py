import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from Configs import configuration
from schemas import Users

config = configuration()

api = config["API"]

logger = logging.getLogger(__name__)

def change_state(user_id, state):
    try:
        logger.debug(f"Verifying state {state} ...")

        if state == "pending" or "verified" or "suspended":
            pass
        else:
            logger.error(f"invalid state {state}")
            raise Unauthorized()

        logger.debug(f"finding user {user_id} ...")
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
            logger.error(f"Multiple users {user_id} found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No user {user_id} found")
            raise Unauthorized()

        logger.debug(f"updating state {state} for user {user_id} ...")
        upd_state = Users.update(state=state).where(
            Users.id == user_id
        )
        upd_state.execute()

        logger.info(f"SUCCESSFULLY UPDATED STATE FOR {user_id}")
        return True
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED UPDATING STATE FOR USER {user_id} CHECK LOGS")
        raise InternalServerError(err)
