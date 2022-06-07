import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.regions import Regions

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def find_region(region_id: str) -> dict:
    """
    Find a region.

    Arguments:
        region_id: str
    
    Returns:
        dict
    """
    try:
        logger.debug("finding region %s ..." % region_id)
        
        regions = (
            Regions.select()
            .where(Regions.id == region_id)
            .dicts()
        )

        result = []

        for region in regions.iterator():
            result.append(region)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple regions %s found" % region_id)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No region found")
            raise Unauthorized()

        logger.info("- Region %s found" % region_id)

        return result[0]

    except DatabaseError as err:
        logger.error("failed to find region %s check logs" % region_id)
        raise InternalServerError(err) from None
