import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from schemas.records.records import Records

from datetime import date

from werkzeug.exceptions import InternalServerError

def find_record(site_id: int, region_id: int, records_user_id: int, permitted_decrypted_data: bool) -> list:
    """
    Find records >= today by site_id and region_id.

    Arguments:
        site_id: int,
        region_id: int,
        records_user_id: int,
        permitted_decrypted_data; bool

    Returns:
        list
    """
    try:
        logger.debug("finding records for %d ..." % records_user_id)
        result = []
        
        records = (
            Records.select(
                Records.record_id,
                Records.records_name,
                Records.records_date,
                Records.records_sex,
                Records.records_date_of_test_request,
                Records.iv
            )
            .where(Records.site_id == site_id, Records.region_id == region_id, Records.records_date >= date.today())
            .dicts()
        )

        for record in records.iterator():
            if permitted_decrypted_data:
                iv = record["iv"]
                data = Data()
                result.append({
                    "record_id" : record["record_id"],
                    "records_name" : data.decrypt(record["records_name"], iv),
                    "records_date" : record["records_date"],
                    "records_sex" : record["records_sex"],
                    "records_date_of_test_request" : record["records_date_of_test_request"]
                })
            else:
                result.append({
                    "record_id" : record["record_id"],
                    "records_name" : record["records_name"],
                    "records_date" : record["records_date"],
                    "records_sex" : record["records_sex"],
                    "records_date_of_test_request" : record["records_date_of_test_request"]
                })

        logger.info("- Successfully found records with site_id = %s & region_id = %s requested by user_id = %s" % (site_id, region_id, records_user_id))
        return result

    except DatabaseError as err:
        logger.error("failed to find record for %d check logs" % records_user_id)
        raise InternalServerError(err) from None
