import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict

def create_user(email: str, password: str, phone_number: str, name: str, occupation: str, site_id: int) -> str:
    """
    Add user to database.

    Arguments:
        email: str,
        password: str,
        phone_number: str,
        name: str,
        occupation: str,
        site_id: int

    Returns:
        str
    """
    try:
        try:
            Users.get(Users.email == email)
        except Users.DoesNotExist:
            logger.debug("creating user record for '%s' ..." % email)

            data = Data()
            password_hash = data.hash(password)

            user = Users.create(
                email=email,
                password_hash=password_hash,
                phone_number=phone_number,
                name=name,
                occupation=occupation
            )

            logger.debug("adding user '%s' to site '%d' ..." % (email, site_id))
            Users_sites.create(
                user_id=user.id,
                site_id=site_id
            )

            logger.info("- User '%s' successfully created" % email)
            return str(user)
        else:
            logger.error("user '%s' already has a record" % email)
            raise Conflict()

    except DatabaseError as err:
        logger.error("creating user '%s' failed check logs" % email)
        raise InternalServerError(err) from None
