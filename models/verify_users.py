import logging
logger = logging.getLogger(__name__)

from error import Conflict, InternalServerError, Unauthorized
from security.data import Data

from peewee import DatabaseError
from schemas.users.users import Users

def verify_user(email: str, password: str) -> dict:
    """
    Find user in database by email and password.

    Arguments:
        email: str,
        password: str

    Returns:
        dict
    """
    try:
        logger.debug("verifying user %s ..." % email)
        data = Data()
        hash_password = data.hash(password)
        users = (
            Users.select()
            .where(Users.email == email, Users.password == hash_password, Users.state == "verified")
            .dicts()
        )
        result = []
        for user in users:
            result.append(user)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple users %s found" % email)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No user found")
            raise Unauthorized()

        logger.info("- User %s successfully verified" % email)
        return {
            "uid": result[0]["id"]
        }
    except DatabaseError as err:
        logger.error("verifying user %s failed check logs" % email)
        raise InternalServerError(err)
