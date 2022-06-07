import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.sites import Sites

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def find_site(site_id: str) -> dict:
    """
    Find a site.

    Arguments:
        site_id: str
    
    Returns:
        dict
    """
    try:
        logger.debug("finding site %s ..." % site_id)
        
        sites = (
            Sites.select()
            .where(Sites.id == site_id)
            .dicts()
        )

        result = []

        for site in sites.iterator():
            result.append(site)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple sites %s found" % site_id)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No site found")
            raise Unauthorized()

        logger.info("- Site %s found" % site_id)

        return result[0]

    except DatabaseError as err:
        logger.error("failed to find site %s check logs" % site_id)
        raise InternalServerError(err) from None
