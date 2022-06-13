import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users_sites import Users_sites

from werkzeug.exceptions import InternalServerError

def remove_user_site(users_sites: list, user_id: int) -> None:
    """
    Remove a user's sites.

    Arguments:
        users_sites: list

    Returns:
        None
    """
    try:
        for site_id in users_sites:
            try:
                user_site = Users_sites.get(user_id=user_id, site_id=site_id)
            except Users_sites.DoesNotExist:
                logger.error("no record for user_id=%s and site_id=%s. Nothing to delete" % (user_id, site_id))
            else:
                user_site.delete_instance()
                logger.info("- Sucessfully removed site_id=%s from user_id=%s" % (site_id, user_id))

    except DatabaseError as err:
        logger.error("removing users_sites failed check logs")
        raise InternalServerError(err) from None
