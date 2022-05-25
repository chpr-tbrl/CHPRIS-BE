import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.records.lab import Labs

from datetime import date

from werkzeug.exceptions import InternalServerError

def find_lab(lab_records_id):
    """
    """
    try:
        logger.debug("finding lab records for %d ..." % lab_records_id)
        result = []
        
        labs = (
            Labs.select()
            .where(Labs.lab_records_id == lab_records_id, Labs.lab_date >= date.today())
            .dicts()
        )
        for lab in labs:
            result.append(lab)

        logger.info("- Successfully found lab records for %d" % lab_records_id)
        return result

    except DatabaseError as err:
        logger.error("failed to find lab record for %d check logs" % lab_records_id)
        raise InternalServerError(err) from None
