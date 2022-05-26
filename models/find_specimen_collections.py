import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.specimen_collection import Specimen_collections

from werkzeug.exceptions import InternalServerError

def find_specimen_collection(specimen_collection_records_id: int) -> list:
    """
    Find specimen_collection records >= today by record_id.

    Arguments:
        specimen_collection_records_id: int

    Returns:
        list
    """
    try:
        logger.debug("finding specimen_collection records for %d ..." % specimen_collection_records_id)
        result = []
        
        specimen_collections = (
            Specimen_collections.select()
            .where(Specimen_collections.specimen_collection_records_id == specimen_collection_records_id)
            .dicts()
        )
        for specimen_collection in specimen_collections:
            result.append(specimen_collection)

        logger.info("- Successfully found specimen_collection records for %d" % specimen_collection_records_id)
        return result

    except DatabaseError as err:
        logger.error("failed to find specimen_collection record for %d check logs" % specimen_collection_records_id)
        raise InternalServerError(err) from None
