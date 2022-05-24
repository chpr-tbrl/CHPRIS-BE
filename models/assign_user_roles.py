import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from Configs import configuration
from schemas.users.users import Users

config = configuration()

api = config["API"]

logger = logging.getLogger(__name__)

def assign_role(user_id, role):
    try:
        logger.debug(f"Verifying role {role} ...")

        if role == "admin" or "data_collection":
            pass
        else:
            logger.error(f"invalid role {role}")
            raise Unauthorized()

        logger.debug(f"finding user {user_id} ...")
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
            logger.error(f"Multiple users {user_id} found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No user {user_id} found")
            raise Unauthorized()

        logger.debug(f"updating role {role} for user {user_id} ...")
        upd_state = Users.update(type_of_user=role).where(
            Users.id == user_id
        )
        upd_state.execute()

        logger.info(f"SUCCESSFULLY ASSIGNED ROLE FOR {user_id}")
        return True
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED ASSIGNING ROLE FOR USER {user_id} CHECK LOGS")
        raise InternalServerError(err)
