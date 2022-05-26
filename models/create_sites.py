import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.sites import Sites

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict

def create_site(name: str, region_id: int) -> str:
    """
    Add site to database.

    Arguments:
        name: str,
        region_id: int

    Returns:
        str
    """
    try:
        try:
            Sites.get(Sites.name == name, Sites.region_id == region_id)
        except Sites.DoesNotExist:
            logger.debug("creating site '%s' ..." % name)

            site = Sites.create(name=name, region_id=region_id)

            logger.info("- Site '%s' successfully created" % name)
            return str(site)
        else:
            logger.error("Site '%s' with region_id=%s exist" % (name, region_id))
            raise Conflict()

    except DatabaseError as err:
        logger.error("creating site '%s' failed check logs" % name)
        raise InternalServerError(err) from None
