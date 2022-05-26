import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.sites.sites import Sites

from werkzeug.exceptions import InternalServerError

def get_all_sites(region_id: int) -> list:
    """
    Fetch all sites for a region.

    Arguments:
        region_id: int

    Returns:
        list
    """
    try:
        logger.debug("fetching all site records ...")
        result = []
        
        sites = (
            Sites.select().where(Sites.region_id == region_id)
            .dicts()
        )
        for site in sites:
            result.append(site)

        logger.info("- Successfully fetched all sites")
        return result

    except DatabaseError as err:
        logger.error("failed to fetch all sites check logs")
        raise InternalServerError(err) from None
