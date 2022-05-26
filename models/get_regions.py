import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.regions import Regions

from werkzeug.exceptions import InternalServerError

def get_all_regions() -> list:
    """
    Fetch all regions.

    Arguments:
        None

    Returns:
        list
    """
    try:
        logger.debug("fetching all region records ...")
        result = []
        
        regions = (
            Regions.select()
            .dicts()
        )
        for region in regions:
            result.append(region)

        logger.info("- Successfully fetched all regions")
        return result

    except DatabaseError as err:
        logger.error("failed to fetch all regions check logs")
        raise InternalServerError(err) from None
