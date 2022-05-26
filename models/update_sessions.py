import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]
secure = api["SECURE_COOKIE"]
hour = eval(api["COOKIE_MAXAGE"])

from peewee import DatabaseError

from datetime import datetime, timedelta

from schemas.users.sessions import Sessions

from werkzeug.exceptions import Conflict
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

def update_session(sid: str, unique_identifier: str) -> dict:
    try:
        """
        Update session in database.

        Arguments:
            sid: str,
            unique_identifier: str

        Returns:
            dict
        """
        expires = datetime.now() + timedelta(milliseconds=hour)

        data = {
            "maxAge": hour,
            "secure": eval(secure),
            "httpOnly": True,
            "sameSite": "lax",
        }

        logger.debug(f"Secure cookie: {secure}")
        logger.debug(f"Cookie maxAge: {hour}")

        logger.debug("finding session %s for user %s ..." % (sid, unique_identifier))
        sessions = (
            Sessions.select()
            .where(Sessions.sid == sid, Sessions.unique_identifier == unique_identifier)
            .dicts()
        )
        result = []
        for session in sessions:
            result.append(session)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple sessions %s found" % sid)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No session %s found" % sid)
            raise Unauthorized()

        logger.debug("updating session %s for user %s ..." % (sid, unique_identifier))
        upd_session = Sessions.update(expires=expires, data=str(data)).where(
            Sessions.sid == sid
        )
        upd_session.execute()

        logger.info("- SUCCESSFULLY UPDATED SESSION %s" % sid)
        return {"sid": sid, "uid": unique_identifier, "data": data}

    except DatabaseError as err:
        logger.error("FAILED UPDATING SESSION %s CHECK LOGS" % sid)
        raise InternalServerError(err) from None
