import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.regions import Regions

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict

def create_region(name: str) -> str:
    """
    Add region to database.

    Arguments:
        name: str

    Returns:
        str
    """
    try:
        try:
            Regions.get(Regions.name == name)
        except Regions.DoesNotExist:
            logger.debug("creating region '%s' ..." % name)

            region = Regions.create(name=name)

            logger.info("- Region '%s' successfully created" % name)
            return str(region)
        else:
            logger.error("Region '%s' exist" % name)
            raise Conflict()
      
    except DatabaseError as err:
        logger.error("creating region '%s' failed check logs" % name)
        raise InternalServerError(err) from None
