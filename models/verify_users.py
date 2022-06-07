import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from schemas.users.users import Users

from models.find_users import find_user

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

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
        
        try:
            user = Users.get(Users.email == email, Users.password_hash == hash_password, Users.account_status == "approved")
        except Users.DoesNotExist:
            logger.error("No user found")
            raise Unauthorized()
        else:
            result = find_user(user.id)

            logger.info("- User %s successfully verified" % email)
            return result
        
    except DatabaseError as err:
        logger.error("verifying user %s failed check logs" % email)
        raise InternalServerError(err) from None
