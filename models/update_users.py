import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

def update_user(id: int, occupation: str, phone_number: str, region_id: int, site_id: int, state: str, type_of_export: str, type_of_user: str, exportable_range: int) -> str:
    """
    Update a user's account.

    Arguments:
        id: int,
        occupation: str,
        phone_number: str,
        region_id: int,
        site_id: int,
        state: str,
        type_of_export: str,
        type_of_user: str,
        exportable_range: str

    Returns:
        str
    """
    try:
        if not state in ["pending", "verified", "suspended"]:
            logger.error("invalid state '%s'" % state)
            raise Unauthorized()   

        logger.debug("Updating user %d record ..." % id)
        
        user = Users.update(occupation=occupation , phone_number=phone_number , region_id=region_id , site_id=site_id , state=state , type_of_export=type_of_export , type_of_user=type_of_user, exportable_range=exportable_range).where(Users.id == id)
        user.execute()

        logger.info("- Successfully updated user %s" % id)
        return str(id)

    except DatabaseError as err:
        logger.error("failed to update users %d check logs" % id)
        raise InternalServerError(err) from None
