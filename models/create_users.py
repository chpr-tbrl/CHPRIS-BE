import logging
logger = logging.getLogger(__name__)

from error import InternalServerError, Conflict
from security.data import Data

from peewee import DatabaseError, IntegrityError
from schemas.users.users import Users

def create_user(email: str, password: str, phone_number: str, name: str, region: str, occupation: str, site: str) -> str:
    """
    Add user to database.

    Arguments:
        email: str,
        password: str,
        phone_number: str,
        name: str,
        region: str,
        occupation: str,
        site: str

    Returns:
        str
    """
    try:
        logger.debug("creating user record for %s ..." % email)
        
        data = Data()
        password_hash = data.hash(password)

        user = Users.create(
            email=email,
            password=password_hash,
            phone_number=phone_number,
            name=name,
            region=region,
            occupation=occupation,
            site=site
        )
        logger.info("- User %s successfully created" % email)
        return str(user)
    except IntegrityError as err:
        logger.error("user %s already has a record" % email)
        raise Conflict()
    except DatabaseError as err:
        logger.error("creating user %s failed check logs" % email)
        raise InternalServerError(err)
