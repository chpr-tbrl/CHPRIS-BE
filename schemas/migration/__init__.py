import logging
logger = logging.getLogger(__name__)

from playhouse.migrate import MySQLMigrator
from playhouse.migrate import migrate

from peewee import OperationalError

from schemas.records.baseModel import records_db
from schemas.records.lab import Labs

from schemas.sites.baseModel import sites_db
from schemas.sites.regions import Regions

record_migrator = MySQLMigrator(records_db)
site_migrator = MySQLMigrator(sites_db)

def migrate_labs() -> None:
    """
    """
    try:
        logger.debug("Starting labs schema migration ...")
        migrate(
            record_migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_result_2', Labs.lab_xpert_mtb_rif_assay_result_2),
            record_migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_grades_2', Labs.lab_xpert_mtb_rif_assay_grades_2),
            record_migrator.add_column('labs', 'lab_xpert_mtb_rif_assay_rif_result_2', Labs.lab_xpert_mtb_rif_assay_rif_result_2),
        )

        logger.info("- Successfully migrated labs schema")

    except OperationalError as error:
        logger.error(error)

def migrate_regions() -> None:
    """
    """
    try:
        logger.debug("Starting regions schema migration ...")
        migrate(
            site_migrator.add_column('regions', 'region_code', Regions.region_code),
        )

        logger.info("- Successfully migrated regions schema")

    except OperationalError as error:
        logger.error(error)
