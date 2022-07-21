import logging
logger = logging.getLogger(__name__)

from playhouse.migrate import MySQLMigrator
from playhouse.migrate import migrate

from peewee import OperationalError

from schemas.records.baseModel import records_db

migrator = MySQLMigrator(records_db)

from schemas.records.lab import Labs

def migrate_labs() -> None:
    """
    """
    try:
        logger.debug("Starting labs schema migration ...")
        migrate(
            migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_result_2', Labs.lab_xpert_mtb_rif_assay_result_2),
            migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_grades_2', Labs.lab_xpert_mtb_rif_assay_grades_2),
            migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_rif_result_2', Labs.lab_xpert_mtb_rif_assay_rif_result_2),
        )

        logger.info("- Successfully migrated labs schema")

    except OperationalError as error:
        logger.error(error)
