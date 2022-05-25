import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.specimen_collection import Specimen_collections

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_specimen_collection(specimen_collection_records_id: int, specimen_collection_user_id: int, specimen_collection_1_date: str, specimen_collection_1_specimen_collection_type: str, specimen_collection_1_other: str, specimen_collection_1_period: str, specimen_collection_1_aspect: str, specimen_collection_1_received_by: str, specimen_collection_2_date: str, specimen_collection_2_specimen_collection_type: str, specimen_collection_2_other: str, specimen_collection_2_period: str, specimen_collection_2_aspect: str, specimen_collection_2_received_by: str) -> str:
    """
    Create a new specimen_collections record.

    Arguments:
        specimen_collection_records_id: int,
        specimen_collection_user_id: int,
        specimen_collection_1_date: str,
        specimen_collection_1_specimen_collection_type: str,
        specimen_collection_1_other: str,
        specimen_collection_1_period: str,
        specimen_collection_1_aspect: str,
        specimen_collection_1_received_by: str,
        specimen_collection_2_date: str,
        specimen_collection_2_specimen_collection_type: str,
        specimen_collection_2_other: str,
        specimen_collection_2_period: str,
        specimen_collection_2_aspect: str,
        specimen_collection_2_received_by: str
            
    Returns:
        str
    """
    try:
        logger.debug("creating specimen_collection record for %d ..." % specimen_collection_user_id)
        
        specimen_collection = Specimen_collections.create(
            specimen_collection_records_id=specimen_collection_records_id,
            specimen_collection_user_id=specimen_collection_user_id,
            specimen_collection_1_date=specimen_collection_1_date,
            specimen_collection_1_specimen_collection_type=specimen_collection_1_specimen_collection_type,
            specimen_collection_1_other=specimen_collection_1_other,
            specimen_collection_1_period=specimen_collection_1_period,
            specimen_collection_1_aspect=specimen_collection_1_aspect,
            specimen_collection_1_received_by=specimen_collection_1_received_by,
            specimen_collection_2_date=specimen_collection_2_date,
            specimen_collection_2_specimen_collection_type=specimen_collection_2_specimen_collection_type,
            specimen_collection_2_other=specimen_collection_2_other,
            specimen_collection_2_period=specimen_collection_2_period,
            specimen_collection_2_aspect=specimen_collection_2_aspect,
            specimen_collection_2_received_by=specimen_collection_2_received_by
        )

        logger.info("- Specimen_collection record %s successfully created" % specimen_collection)
        return str(specimen_collection)

    except OperationalError as error:
        logger.error(error)
        raise BadRequest()

    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
        
    except DatabaseError as err:
        logger.error("creating Specimen_collection record failed check logs")
        raise InternalServerError(err) from None
