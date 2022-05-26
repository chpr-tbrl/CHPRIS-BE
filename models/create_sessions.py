import logging
logger = logging.getLogger(__name__)

from error import InternalServerError

from Configs import baseConfig
config = baseConfig()
api = config["API"]
secure = api["SECURE_COOKIE"]
hour = eval(api["COOKIE_MAXAGE"])

from peewee import DatabaseError
from uuid import uuid4
from datetime import datetime, timedelta
from schemas.users.sessions import Sessions

def create_session(unique_identifier: str, user_agent: str) -> dict:
    """
    Create session in database.

    Arguments:
        unique_identifier: str,
        user_agent: str

    Returns:
        dict
    """
    try:
        expires = datetime.now() + timedelta(milliseconds=hour)

        data = {
            "maxAge": hour,
            "secure": eval(secure),
            "httpOnly": True,
            "sameSite": "lax",
        }

        logger.debug("Secure cookie: %s" % secure)
        logger.debug("Cookie maxAge: %s" % hour)

        logger.debug("creating session for %s ..." % unique_identifier)
        session = Sessions.create(
            sid=uuid4(),
            unique_identifier=unique_identifier,
            user_agent=user_agent,
            expires=expires,
            data=str(data),
            createdAt=datetime.now(),
        )
        logger.info(
            "- SUCCESSFULLY CREATED SESSION %s FOR %s" % (str(session), unique_identifier) 
        )
        return {"sid": str(session), "uid": unique_identifier, "data": data}

    except DatabaseError as err:
        logger.error("FAILED TO CREATE SESSION FOR %s CHECK LOGS" % unique_identifier)
        raise InternalServerError(err) from None
