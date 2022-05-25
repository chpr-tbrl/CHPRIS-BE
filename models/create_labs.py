import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError
from peewee import OperationalError
from peewee import IntegrityError

from schemas.records.lab import Labs

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

def create_lab(lab_records_id: int, lab_user_id: int, lab_date_specimen_collection_received: str, lab_received_by: str, lab_registration_number: str, lab_smear_microscopy_result_result_1: str, lab_smear_microscopy_result_result_2: str, lab_smear_microscopy_result_date: str, lab_smear_microscopy_result_done_by: str, lab_xpert_mtb_rif_assay_result: str, lab_xpert_mtb_rif_assay_grades: str, lab_xpert_mtb_rif_assay_rif_result: str, lab_xpert_mtb_rif_assay_date: str, lab_xpert_mtb_rif_assay_done_by: str, lab_urine_lf_lam_result: str, lab_urine_lf_lam_date: str, lab_urine_lf_lam_done_by: str) -> str:
    """
    """
    try:
        logger.debug("creating lab record for %d ..." % lab_user_id)
        
        lab = Labs.create(
            lab_records_id=lab_records_id,
            lab_user_id=lab_user_id,
            lab_date_specimen_collection_received=lab_date_specimen_collection_received,
            lab_received_by=lab_received_by,
            lab_registration_number=lab_registration_number,
            lab_smear_microscopy_result_result_1=lab_smear_microscopy_result_result_1,
            lab_smear_microscopy_result_result_2=lab_smear_microscopy_result_result_2,
            lab_smear_microscopy_result_date=lab_smear_microscopy_result_date,
            lab_smear_microscopy_result_done_by=lab_smear_microscopy_result_done_by,
            lab_xpert_mtb_rif_assay_result=lab_xpert_mtb_rif_assay_result,
            lab_xpert_mtb_rif_assay_grades=lab_xpert_mtb_rif_assay_grades,
            lab_xpert_mtb_rif_assay_rif_result=lab_xpert_mtb_rif_assay_rif_result,
            lab_xpert_mtb_rif_assay_date=lab_xpert_mtb_rif_assay_date,
            lab_xpert_mtb_rif_assay_done_by=lab_xpert_mtb_rif_assay_done_by,
            lab_urine_lf_lam_result=lab_urine_lf_lam_result,
            lab_urine_lf_lam_date=lab_urine_lf_lam_date,
            lab_urine_lf_lam_done_by=lab_urine_lf_lam_done_by
        )

        logger.info("- Lab record %s successfully created" % lab)
        return str(lab)

    except OperationalError as error:
        logger.error(error)
        raise BadRequest()

    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()

    except DatabaseError as err:
        logger.error("creating Lab record %s failed check logs" % lab)
        raise InternalServerError(err) from None
