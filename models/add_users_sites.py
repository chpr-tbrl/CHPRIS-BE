import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import IntegrityError

from schemas.users.users_sites import Users_sites

from werkzeug.exceptions import InternalServerError

def add_user_site(users_sites: list, user_id: int) -> None:
    """
    Add a user's sites.

    Arguments:
        users_sites: list

    Returns:
        None
    """
    try:
        for site_id in users_sites:
            try:
                Users_sites.create(user_id=user_id, site_id=site_id)
                logger.info("- Successfully added site_id=%s to user_id=%s" % (site_id, user_id))
            except IntegrityError as error:
                logger.error(error)

    except DatabaseError as err:
        logger.error("creating users_sites failed check logs")
        raise InternalServerError(err) from None
