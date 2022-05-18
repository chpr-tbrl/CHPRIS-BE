import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError, IntegrityError
from schemas.records.specimen_collection import Specimen_collection

logger = logging.getLogger(__name__)

def create_specimen_collection(
    specimen_collection_records_id,
    specimen_collection_user_id,
    specimen_collection_1_date,
    specimen_collection_1_specimen_collection_type,
    specimen_collection_1_other,
    specimen_collection_1_period,
    specimen_collection_1_aspect,
    specimen_collection_1_received_by,
    specimen_collection_2_date,
    specimen_collection_2_specimen_collection_type,
    specimen_collection_2_other,
    specimen_collection_2_period,
    specimen_collection_2_aspect,
    specimen_collection_2_received_by,
    ):
    try:
        logger.debug(f"creating specimen_collection record for {specimen_collection_user_id} ...")

        if not specimen_collection_1_specimen_collection_type in ["sputum", "csf", "lymph_node_aspirate", "gastric_aspirate", "urine", "other"]:
            logger.error(f"specimen_collection_1_specimen_collection_type got invalid value '{specimen_collection_1_specimen_collection_type}'")
            raise BadRequest()
        if not specimen_collection_1_period in ["spot", "morning", "n_a"]:
            logger.error(f"specimen_collection_1_period got invalid value '{specimen_collection_1_period}'")
            raise BadRequest()
        if not specimen_collection_1_aspect in ["mucopurulent", "bloody", "salivary","n_a"]:
            logger.error(f"specimen_collection_1_aspect got invalid value '{specimen_collection_1_aspect}'")
            raise BadRequest()
        if not specimen_collection_2_specimen_collection_type in ["sputum", "csf", "lymph_node_aspirate", "gastric_aspirate", "urine", "other"]:
            logger.error(f"specimen_collection_2_specimen_collection_type got invalid value '{specimen_collection_2_specimen_collection_type}'")
            raise BadRequest()
        if not specimen_collection_2_period in ["spot", "morning", "n_a"]:
            logger.error(f"specimen_collection_2_period got invalid value '{specimen_collection_2_period}'")
            raise BadRequest()
        if not specimen_collection_2_aspect in ["mucopurulent", "bloody", "salivary","n_a"]:
            logger.error(f"specimen_collection_2_aspect got invalid value '{specimen_collection_2_aspect}'")
            raise BadRequest()
        
        specimen_collection = Specimen_collection.create(
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

        logger.info(f"Specimen_collection record {specimen_collection} successfully created")
        return str(specimen_collection)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating Specimen_collection record {specimen_collection} failed check logs")
        raise InternalServerError(err)
