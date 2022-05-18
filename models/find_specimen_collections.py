import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

from peewee import DatabaseError
from schemas.records.specimen_collection import Specimen_collection

logger = logging.getLogger(__name__)

def find_specimen_collection(specimen_collection_user_id, specimen_collection_records_id):
    try:
        logger.debug(f"finding specimen_collection records for {specimen_collection_user_id} ...")
        result = []
        
        specimen_collections = (
            Specimen_collection.select()
            .where(Specimen_collection.specimen_collection_user_id == specimen_collection_user_id, Specimen_collection.specimen_collection_records_id == specimen_collection_records_id)
            .dicts()
        )
        for specimen_collection in specimen_collections:
            result.append(specimen_collection)

        logger.info(f"Successfully found specimen_collection records for {specimen_collection_user_id}")
        return result
    except DatabaseError as err:
        logger.error(f"failed to finding specimen_collection record for {specimen_collection_user_id} check logs")
        raise InternalServerError(err)
