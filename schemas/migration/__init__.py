import logging
logger = logging.getLogger(__name__)

from playhouse.migrate import MySQLMigrator
from playhouse.migrate import migrate

from peewee import OperationalError

from schemas.records.baseModel import records_db
from schemas.records.records import Records
from schemas.records.lab import Labs

from schemas.sites.baseModel import sites_db
from schemas.sites.regions import Regions

record_migrator = MySQLMigrator(records_db)
site_migrator = MySQLMigrator(sites_db)

# def migrate_records() -> None:
#     """
#     """
#     try:
#         logger.debug("Starting records schema migration ...")
#         migrate(
#             record_migrator.drop_column('records', 'records_tb_treatment_history_contact_of_tb_patient'),
#             record_migrator.add_column('records', 'records_tb_treatment_history_contact_of_tb_patient', Records.records_tb_treatment_history_contact_of_tb_patient),
#             record_migrator.add_column('records', 'records_tb_treatment_history_other', Records.records_tb_treatment_history_other),
#             record_migrator.add_column('records', 'records_patient_category_prisoner', Records.records_patient_category_prisoner),
#         )

#         logger.info("- Successfully migrated records schema")

#     except OperationalError as error:
#         logger.error(error)

def migrate_labs() -> None:
    """
    """
    try:
        logger.debug("Starting labs schema migration ...")
        migrate(
            record_migrator.add_column('labs', 'lab_culture_date', Labs.lab_culture_date),
            record_migrator.add_column('labs', 'lab_culture_done_by', Labs.lab_culture_done_by),
            record_migrator.add_column('labs', 'lab_lpa_date', Labs.lab_lpa_date),
            record_migrator.add_column('labs', 'lab_lpa_done_by', Labs.lab_lpa_done_by),
            record_migrator.add_column('labs', 'lab_dst_date', Labs.lab_dst_date),
            record_migrator.add_column('labs', 'lab_dst_done_by', Labs.lab_dst_done_by),
        )

        logger.info("- Successfully migrated labs schema")

    except OperationalError as error:
        logger.error(error)