import logging
logger = logging.getLogger(__name__)

import requests

# configurations
from Configs import baseConfig
config = baseConfig()
smswithoutborders = config["SMSWITHOUTBORDERS"]

from werkzeug.exceptions import InternalServerError

class SMS_Model:
    """
    """
    def __init__(self) -> None:
        self.openapi_url = smswithoutborders["OPENAPI_URL"]
        self.enable_sms = smswithoutborders["ENABLE_SMS"]
        self.auth_id = smswithoutborders["AUTH_ID"]

        if not self.openapi_url:
            raise ValueError("Set OPENAPI_URL in configs file")
        elif not self.enable_sms:
            raise ValueError("Set ENABLE_SMS in configs file")
        elif not self.auth_id:
            raise ValueError("Set AUTH_ID in configs file")

    def send_lab(self, records: dict, labs: dict, contacts: list) -> None:
        """
        """
        try:
            record_id = records["record_id"]
            records_name = records["records_name"].split(" ")
            records_date_of_test_request = records["records_date_of_test_request"]

            lab_smear_microscopy_result_result_1 = labs["lab_smear_microscopy_result_result_1"]
            lab_smear_microscopy_result_result_2 = labs["lab_smear_microscopy_result_result_2"]
            lab_xpert_mtb_rif_assay_result = labs["lab_xpert_mtb_rif_assay_result"]
            lab_xpert_mtb_rif_assay_grades = labs["lab_xpert_mtb_rif_assay_grades"]
            lab_xpert_mtb_rif_assay_rif_result = labs["lab_xpert_mtb_rif_assay_rif_result"]
            lab_urine_lf_lam_result = labs["lab_urine_lf_lam_result"]
            info_line = "+237670656041"

            record_name = "%s%s" % (records_name[0], "" if len(records_name)<2 else " %s." % records_name[1])
            logger.debug["record_name: %s" % record_name]

            if lab_smear_microscopy_result_result_2 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_2
            elif lab_smear_microscopy_result_result_1 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_1
            else:
                smr_result = lab_smear_microscopy_result_result_2

            logger.debug["lab_smear_microscopy_result_result_1: %s" % lab_smear_microscopy_result_result_1]
            logger.debug["lab_smear_microscopy_result_result_2: %s" % lab_smear_microscopy_result_result_1]
            logger.debug["smr_result: %s" % smr_result]

            if lab_xpert_mtb_rif_assay_result in ["detected", "trace",]:
                grade = lab_xpert_mtb_rif_assay_grades
            else:
                grade = None

            logger.debug["lab_xpert_mtb_rif_assay_result: %s" % lab_xpert_mtb_rif_assay_result]
            logger.debug["lab_xpert_mtb_rif_assay_grades: %s" % lab_xpert_mtb_rif_assay_grades]
            logger.debug["grade: %s" % grade]

            sms_result = self.__lab_schema__(records_date_of_test_request=records_date_of_test_request, record_id=record_id, records_name=record_name, smr_result=smr_result, lab_xpert_mtb_rif_assay_result=lab_xpert_mtb_rif_assay_result, lab_xpert_mtb_rif_assay_grades=grade, lab_xpert_mtb_rif_assay_rif_result=lab_xpert_mtb_rif_assay_rif_result, lab_urine_lf_lam_result=lab_urine_lf_lam_result, info_line=info_line)

            logger.debug("SMS_result: %s" % sms_result)
            
            if self.enable_sms:
                self.__send_sms_message__(text=sms_result, contacts=contacts)
                return None
            else:
                return None

        except Exception as error:
            raise InternalServerError(error) from None

    def __lab_schema__(self, records_date_of_test_request: str, record_id: int, records_name: str, smr_result: str, lab_xpert_mtb_rif_assay_result: str, lab_xpert_mtb_rif_assay_grades: str, lab_xpert_mtb_rif_assay_rif_result: str, lab_urine_lf_lam_result: str, info_line: str) -> str:
        """
        """
        try:
            schema = """%s\n
                        %s\n
                        %s\n
                        AFB, %s\n
                        XPERT, %s%s, %s\n
                        URINE, %s\n
                        INFO %s
                    """ % (
                        records_date_of_test_request,
                        record_id,
                        records_name,
                        smr_result,
                        lab_xpert_mtb_rif_assay_result, "" if not lab_xpert_mtb_rif_assay_grades else " (%s)" % lab_xpert_mtb_rif_assay_grades, lab_xpert_mtb_rif_assay_rif_result,
                        lab_urine_lf_lam_result,
                        info_line
                    )

            return schema

        except Exception as error:
            raise InternalServerError(error) from None

    def __send_sms_message__(self, text: str, contacts: list) -> None:
        """
        """
        sms_url = f"{self.openapi_url}//v1/sms"
        operator_url = f"{self.openapi_url}//v1/sms/operators"
        auth_id = self.auth_id

        payload = []

        for contact in contacts:
            payload.append({
                "operator_name":"",
                "text":text,
                "number":contact
            })

        try:
            operator_res = requests.post(url=operator_url, json=payload)

            if operator_res.status_code == 200:
                logger.info("- Successfully fetched operator names.")

                operator_data = operator_res.json()

                sms_data = {
                    "auth_id":auth_id,
                    "data": operator_data,
                    "callback_url": ""
                    }
                
                sms_res = requests.post(url=sms_url, json=sms_data)

                if sms_res.status_code == 200:
                    logger.info("- Successfully sent.")
                    return None
                else:
                    logger.error("- Cannot send SMS")
                    raise InternalServerError(sms_res.text)    

            else:
                logger.error("- Cannot get operator_name")
                raise InternalServerError(operator_res.text)

        except Exception as error:
            raise InternalServerError(error)


