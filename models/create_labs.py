import logging

from error import BadRequest, InternalServerError

from peewee import DatabaseError, OperationalError, IntegrityError
from schemas.records.lab import Labs

logger = logging.getLogger(__name__)

def create_lab(
    lab_records_id,
    lab_user_id,
    lab_date_specimen_collection_received,
    lab_received_by,
    lab_registration_number,
    lab_smear_microscopy_result_result_1,
    lab_smear_microscopy_result_result_2,
    lab_smear_microscopy_result_date,
    lab_smear_microscopy_result_done_by,
    lab_xpert_mtb_rif_assay_result,
    lab_xpert_mtb_rif_assay_grades,
    lab_xpert_mtb_rif_assay_rif_result,
    lab_xpert_mtb_rif_assay_date,
    lab_xpert_mtb_rif_assay_done_by,
    lab_urine_lf_lam_result,
    lab_urine_lf_lam_date,
    lab_urine_lf_lam_done_by,
    ):
    try:
        logger.debug(f"creating lab record for {lab_user_id} ...")

        if not lab_smear_microscopy_result_result_1 in ["no_afb_seen", "scanty", "1+", "2+", "3+", "tb_lamp_positive", "tb_lamp_negative", "not_done"]:
            logger.error(f"lab_smear_microscopy_result_result_1 got invalid value '{lab_smear_microscopy_result_result_1}'")
            raise BadRequest()
        if not lab_smear_microscopy_result_result_2 in ["no_afb_seen", "scanty", "1+", "2+", "3+", "tb_lamp_positive", "tb_lamp_negative", "not_done"]:
            logger.error(f"lab_smear_microscopy_result_result_2 got invalid value '{lab_smear_microscopy_result_result_2}'")
            raise BadRequest()
        if not lab_xpert_mtb_rif_assay_result in ["detected", "trace", "not_detected", "error_invalid", "not_done"]:
            logger.error(f"lab_xpert_mtb_rif_assay_result got invalid value '{lab_xpert_mtb_rif_assay_result}'")
            raise BadRequest()
        if not lab_xpert_mtb_rif_assay_grades in ["high", "medium", "low", "very_low"]:
            logger.error(f"lab_xpert_mtb_rif_assay_grades got invalid value '{lab_xpert_mtb_rif_assay_grades}'")
            raise BadRequest()
        if not lab_xpert_mtb_rif_assay_rif_result in ["detected", "indeterminate", "not_detected", "not_done"]:
            logger.error(f"lab_xpert_mtb_rif_assay_rif_result got invalid value '{lab_xpert_mtb_rif_assay_rif_result}'")
            raise BadRequest()
        if not lab_urine_lf_lam_result in ["negative", "positive", "error_invalid", "not_done"]:
            logger.error(f"lab_urine_lf_lam_result got invalid value '{lab_urine_lf_lam_result}'")
            raise BadRequest()
        
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

        logger.info(f"Lab record {lab} successfully created")
        return str(lab)
    except OperationalError as error:
        logger.error(error)
        raise BadRequest()
    except IntegrityError as error:
        logger.error(error)
        raise BadRequest()
    except DatabaseError as err:
        logger.error(f"creating Lab record {lab} failed check logs")
        raise InternalServerError(err)
