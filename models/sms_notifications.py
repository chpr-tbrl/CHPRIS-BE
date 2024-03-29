import logging
logger = logging.getLogger(__name__)

import requests

from security.data import Data

# configurations
from Configs import baseConfig
config = baseConfig()
smswithoutborders = config["SMSWITHOUTBORDERS"]

from schemas.records.records import Records
from schemas.records.lab import Labs

from werkzeug.exceptions import InternalServerError

class SMS_Model:
    """
    """
    def __init__(self) -> None:
        if not smswithoutborders["OPENAPI_URL"]:
            raise ValueError("Set OPENAPI_URL in configs file")
        elif not smswithoutborders["ENABLE_SMS"]:
            raise ValueError("Set ENABLE_SMS in configs file")
        elif not smswithoutborders["AUTH_ID"]:
            raise ValueError("Set AUTH_ID in configs file")

        self.openapi_url = smswithoutborders["OPENAPI_URL"]
        self.enable_sms = eval(smswithoutborders["ENABLE_SMS"])
        self.auth_id = smswithoutborders["AUTH_ID"]
        self.Records = Records
        self.Labs = Labs
        self.Data = Data

    def send_lab(self, record_id: int, lab_id: int, contacts: list) -> None:
        """
        """
        try:
            result = []
            
            query = (
                self.Records.select(
                    self.Records.records_name,
                    self.Records.records_date_of_test_request,
                    self.Records.iv,
                    self.Labs.lab_smear_microscopy_result_result_1,
                    self.Labs.lab_smear_microscopy_result_result_2,
                    self.Labs.lab_xpert_mtb_rif_assay_result,
                    self.Labs.lab_xpert_mtb_rif_assay_grades,
                    self.Labs.lab_xpert_mtb_rif_assay_rif_result,
                    self.Labs.lab_xpert_mtb_rif_assay_result_2,
                    self.Labs.lab_xpert_mtb_rif_assay_grades_2,
                    self.Labs.lab_xpert_mtb_rif_assay_rif_result_2,
                    self.Labs.lab_urine_lf_lam_result
                )
                .where(
                    self.Records.record_id == record_id
                )
                .join(self.Labs)
                .where(
                    self.Labs.lab_id == lab_id
                )
            )

            for record in query.iterator():
                iv = record.iv

                data = self.Data()

                result.append({
                    "records_name": data.decrypt(record.records_name, iv),
                    "records_date_of_test_request": record.records_date_of_test_request,
                    "lab_smear_microscopy_result_result_1": record.labs.lab_smear_microscopy_result_result_1,
                    "lab_smear_microscopy_result_result_2": record.labs.lab_smear_microscopy_result_result_2,
                    "lab_xpert_mtb_rif_assay_result": record.labs.lab_xpert_mtb_rif_assay_result,
                    "lab_xpert_mtb_rif_assay_grades": record.labs.lab_xpert_mtb_rif_assay_grades,
                    "lab_xpert_mtb_rif_assay_rif_result": record.labs.lab_xpert_mtb_rif_assay_rif_result,
                    "lab_xpert_mtb_rif_assay_result_2": record.labs.lab_xpert_mtb_rif_assay_result_2,
                    "lab_xpert_mtb_rif_assay_grades_2": record.labs.lab_xpert_mtb_rif_assay_grades_2,
                    "lab_xpert_mtb_rif_assay_rif_result_2": record.labs.lab_xpert_mtb_rif_assay_rif_result_2,
                    "lab_urine_lf_lam_result": record.labs.lab_urine_lf_lam_result
                })

            records_name = result[0]["records_name"].split()
            records_date_of_test_request = result[0]["records_date_of_test_request"]

            lab_smear_microscopy_result_result_1 = result[0]["lab_smear_microscopy_result_result_1"].lower() if result[0]["lab_smear_microscopy_result_result_1"] else None
            lab_smear_microscopy_result_result_2 = result[0]["lab_smear_microscopy_result_result_2"].lower() if result[0]["lab_smear_microscopy_result_result_2"] else None
            lab_xpert_mtb_rif_assay_result = result[0]["lab_xpert_mtb_rif_assay_result"].lower() if result[0]["lab_xpert_mtb_rif_assay_result"] else None
            lab_xpert_mtb_rif_assay_grades = result[0]["lab_xpert_mtb_rif_assay_grades"].lower() if result[0]["lab_xpert_mtb_rif_assay_grades"] else None
            lab_xpert_mtb_rif_assay_rif_result = result[0]["lab_xpert_mtb_rif_assay_rif_result"].lower() if result[0]["lab_xpert_mtb_rif_assay_rif_result"] else None
            lab_xpert_mtb_rif_assay_result_2 = result[0]["lab_xpert_mtb_rif_assay_result_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_result_2"] else None
            lab_xpert_mtb_rif_assay_grades_2 = result[0]["lab_xpert_mtb_rif_assay_grades_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_grades_2"] else None
            lab_xpert_mtb_rif_assay_rif_result_2 = result[0]["lab_xpert_mtb_rif_assay_rif_result_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_rif_result_2"] else None
            lab_urine_lf_lam_result = result[0]["lab_urine_lf_lam_result"].lower() if result[0]["lab_urine_lf_lam_result"] else None
            info_line = "670656041"
            
            record_name = "%s%s" % (records_name[0], "" if len(records_name)<2 else " %s." % records_name[1][0])
            logger.debug("record_name: %s" % record_name)

            if lab_smear_microscopy_result_result_2 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_2
            elif lab_smear_microscopy_result_result_1 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_1
            elif lab_smear_microscopy_result_result_2 in ["not_done"]:
                smr_result = lab_smear_microscopy_result_result_1
            else:
                smr_result = lab_smear_microscopy_result_result_2

            if lab_xpert_mtb_rif_assay_result_2 in ["detected"]:
                xpert_result = lab_xpert_mtb_rif_assay_result_2
                xpert_grade = lab_xpert_mtb_rif_assay_grades_2
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result_2
            elif lab_xpert_mtb_rif_assay_result in ["detected"]:
                xpert_result = lab_xpert_mtb_rif_assay_result
                xpert_grade = lab_xpert_mtb_rif_assay_grades
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result
            elif lab_xpert_mtb_rif_assay_result_2 in ["not_done"]:
                xpert_result = lab_xpert_mtb_rif_assay_result
                xpert_grade = lab_xpert_mtb_rif_assay_grades
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result
            else:
                xpert_result = lab_xpert_mtb_rif_assay_result_2
                xpert_grade = lab_xpert_mtb_rif_assay_grades_2
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result_2

            logger.debug("lab_smear_microscopy_result_result_1: %s" % lab_smear_microscopy_result_result_1)
            logger.debug("lab_smear_microscopy_result_result_2: %s" % lab_smear_microscopy_result_result_2)
            logger.debug("smr_result: %s" % smr_result)

            if xpert_result in ["detected"]:
                grade = xpert_grade
            else:
                grade = None

            logger.debug("lab_xpert_mtb_rif_assay_result: %s" % xpert_result)
            logger.debug("lab_xpert_mtb_rif_assay_grades: %s" % xpert_grade)
            logger.debug("grade: %s" % grade)

            sms_result = self.__lab_schema__(records_date_of_test_request=records_date_of_test_request, record_id=record_id, records_name=record_name, smr_result=smr_result, lab_xpert_mtb_rif_assay_result=xpert_result, lab_xpert_mtb_rif_assay_grades=grade, lab_xpert_mtb_rif_assay_rif_result=xpert_rif_result, lab_urine_lf_lam_result=lab_urine_lf_lam_result, info_line=info_line)

            logger.debug("SMS_result: %s" % sms_result)
            
            if self.enable_sms:
                self.__send_sms_message__(text=sms_result, contacts=contacts)
                return None
            elif self.enable_sms:
                return None

        except Exception as error:
            raise InternalServerError(error)

    def send_requester(self, record_id: int, lab_id: int, contacts: list) -> None:
        """
        """
        try:
            result = []
            
            query = (
                self.Records.select(
                    self.Records.records_name,
                    self.Records.records_date_of_test_request,
                    self.Records.iv,
                    self.Labs.lab_smear_microscopy_result_result_1,
                    self.Labs.lab_smear_microscopy_result_result_2,
                    self.Labs.lab_xpert_mtb_rif_assay_result,
                    self.Labs.lab_xpert_mtb_rif_assay_grades,
                    self.Labs.lab_xpert_mtb_rif_assay_rif_result,
                    self.Labs.lab_xpert_mtb_rif_assay_result_2,
                    self.Labs.lab_xpert_mtb_rif_assay_grades_2,
                    self.Labs.lab_xpert_mtb_rif_assay_rif_result_2,
                    self.Labs.lab_urine_lf_lam_result
                )
                .where(
                    self.Records.record_id == record_id
                )
                .join(self.Labs)
                .where(
                    self.Labs.lab_id == lab_id
                )
            )

            for record in query.iterator():
                iv = record.iv

                data = self.Data()

                result.append({
                    "records_name": data.decrypt(record.records_name, iv),
                    "records_date_of_test_request": record.records_date_of_test_request,
                    "lab_smear_microscopy_result_result_1": record.labs.lab_smear_microscopy_result_result_1,
                    "lab_smear_microscopy_result_result_2": record.labs.lab_smear_microscopy_result_result_2,
                    "lab_xpert_mtb_rif_assay_result": record.labs.lab_xpert_mtb_rif_assay_result,
                    "lab_xpert_mtb_rif_assay_grades": record.labs.lab_xpert_mtb_rif_assay_grades,
                    "lab_xpert_mtb_rif_assay_rif_result": record.labs.lab_xpert_mtb_rif_assay_rif_result,
                    "lab_xpert_mtb_rif_assay_result_2": record.labs.lab_xpert_mtb_rif_assay_result_2,
                    "lab_xpert_mtb_rif_assay_grades_2": record.labs.lab_xpert_mtb_rif_assay_grades_2,
                    "lab_xpert_mtb_rif_assay_rif_result_2": record.labs.lab_xpert_mtb_rif_assay_rif_result_2,
                    "lab_urine_lf_lam_result": record.labs.lab_urine_lf_lam_result
                })

            records_name = result[0]["records_name"].split()
            records_date_of_test_request = result[0]["records_date_of_test_request"]

            lab_smear_microscopy_result_result_1 = result[0]["lab_smear_microscopy_result_result_1"].lower() if result[0]["lab_smear_microscopy_result_result_1"] else None
            lab_smear_microscopy_result_result_2 = result[0]["lab_smear_microscopy_result_result_2"].lower() if result[0]["lab_smear_microscopy_result_result_2"] else None
            lab_xpert_mtb_rif_assay_result = result[0]["lab_xpert_mtb_rif_assay_result"].lower() if result[0]["lab_xpert_mtb_rif_assay_result"] else None
            lab_xpert_mtb_rif_assay_grades = result[0]["lab_xpert_mtb_rif_assay_grades"].lower() if result[0]["lab_xpert_mtb_rif_assay_grades"] else None
            lab_xpert_mtb_rif_assay_rif_result = result[0]["lab_xpert_mtb_rif_assay_rif_result"].lower() if result[0]["lab_xpert_mtb_rif_assay_rif_result"] else None
            lab_xpert_mtb_rif_assay_result_2 = result[0]["lab_xpert_mtb_rif_assay_result_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_result_2"] else None
            lab_xpert_mtb_rif_assay_grades_2 = result[0]["lab_xpert_mtb_rif_assay_grades_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_grades_2"] else None
            lab_xpert_mtb_rif_assay_rif_result_2 = result[0]["lab_xpert_mtb_rif_assay_rif_result_2"].lower() if result[0]["lab_xpert_mtb_rif_assay_rif_result_2"] else None
            lab_urine_lf_lam_result = result[0]["lab_urine_lf_lam_result"].lower() if result[0]["lab_urine_lf_lam_result"] else None
            info_line = "670656041"
            
            record_name = "%s%s" % (records_name[0], "" if len(records_name)<2 else " %s." % records_name[1][0])
            logger.debug("record_name: %s" % record_name)

            if lab_smear_microscopy_result_result_2 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_2
            elif lab_smear_microscopy_result_result_1 in ["scanty", "1+", "2+", "3+"]:
                smr_result = lab_smear_microscopy_result_result_1
            elif lab_smear_microscopy_result_result_2 in ["not_done"]:
                smr_result = lab_smear_microscopy_result_result_1
            else:
                smr_result = lab_smear_microscopy_result_result_2

            if lab_xpert_mtb_rif_assay_result_2 in ["detected"]:
                xpert_result = lab_xpert_mtb_rif_assay_result_2
                xpert_grade = lab_xpert_mtb_rif_assay_grades_2
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result_2
            elif lab_xpert_mtb_rif_assay_result in ["detected"]:
                xpert_result = lab_xpert_mtb_rif_assay_result
                xpert_grade = lab_xpert_mtb_rif_assay_grades
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result
            elif lab_xpert_mtb_rif_assay_result_2 in ["not_done"]:
                xpert_result = lab_xpert_mtb_rif_assay_result
                xpert_grade = lab_xpert_mtb_rif_assay_grades
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result
            else:
                xpert_result = lab_xpert_mtb_rif_assay_result_2
                xpert_grade = lab_xpert_mtb_rif_assay_grades_2
                xpert_rif_result = lab_xpert_mtb_rif_assay_rif_result_2

            logger.debug("lab_smear_microscopy_result_result_1: %s" % lab_smear_microscopy_result_result_1)
            logger.debug("lab_smear_microscopy_result_result_2: %s" % lab_smear_microscopy_result_result_2)
            logger.debug("smr_result: %s" % smr_result)

            if xpert_result in ["detected"]:
                grade = xpert_grade
            else:
                grade = None

            logger.debug("lab_xpert_mtb_rif_assay_result: %s" % xpert_result)
            logger.debug("lab_xpert_mtb_rif_assay_grades: %s" % xpert_grade)
            logger.debug("grade: %s" % grade)

            sms_result = self.__requester_schema__(records_date_of_test_request=records_date_of_test_request, record_id=record_id, records_name=record_name, smr_result=smr_result, lab_xpert_mtb_rif_assay_result=xpert_result, lab_xpert_mtb_rif_assay_grades=grade, lab_xpert_mtb_rif_assay_rif_result=xpert_rif_result, lab_urine_lf_lam_result=lab_urine_lf_lam_result, info_line=info_line)

            logger.debug("SMS_result: %s" % sms_result)
            
            if self.enable_sms:
                self.__send_sms_message__(text=sms_result, contacts=contacts)
                return None
            elif self.enable_sms:
                return None

        except Exception as error:
            raise InternalServerError(error)

    def send_client(self, contacts: list) -> None:
        """
        """
        try:
            sms_result = self.__client_schema__()

            logger.debug("SMS_result: %s" % sms_result)
            
            if self.enable_sms:
                self.__send_sms_message__(text=sms_result, contacts=contacts)
                return None
            elif self.enable_sms:
                return None

        except Exception as error:
            raise InternalServerError(error)

    def __lab_schema__(self, records_date_of_test_request: str, record_id: int, records_name: str, smr_result: str, lab_xpert_mtb_rif_assay_result: str, lab_xpert_mtb_rif_assay_grades: str, lab_xpert_mtb_rif_assay_rif_result: str, lab_urine_lf_lam_result: str, info_line: str) -> str:
        """
        """
        try:
            lab_schema = ""

            lab_schema += "%s\n" % records_date_of_test_request
            lab_schema += "%s\n" % record_id
            lab_schema += "%s\n" % records_name

            if smr_result in ["not_done"]:
                pass
            else:
                lab_schema += "AFB, %s\n" % smr_result.upper().replace("_", " ")

            if lab_xpert_mtb_rif_assay_result in ["not_done", "error_invalid"]:
                pass
            else:
                lab_schema += "XPERT, %s%s%s\n" % (lab_xpert_mtb_rif_assay_result.upper().replace("_", " "), "" if not lab_xpert_mtb_rif_assay_grades else " (%s)" % lab_xpert_mtb_rif_assay_grades.upper().replace("_", " "), "" if lab_xpert_mtb_rif_assay_rif_result in ["not_done", "error_invalid"] else ", RIF RESISTANCE %s" % lab_xpert_mtb_rif_assay_rif_result.upper().replace("_", " "))
            
            if lab_urine_lf_lam_result in ["not_done", "error_invalid"]:
                pass
            else:
                lab_schema += "URINE, %s\n" % lab_urine_lf_lam_result.upper().replace("_", " ")

            lab_schema += "INFO %s" % info_line

            return lab_schema

        except Exception as error:
            raise InternalServerError(error)

    def __requester_schema__(self, records_date_of_test_request: str, record_id: int, records_name: str, smr_result: str, lab_xpert_mtb_rif_assay_result: str, lab_xpert_mtb_rif_assay_grades: str, lab_xpert_mtb_rif_assay_rif_result: str, lab_urine_lf_lam_result: str, info_line: str) -> str:
        """
        """
        try:
            requester_schema = ""

            requester_schema += "%s\n" % records_date_of_test_request
            requester_schema += "%s\n" % record_id
            requester_schema += "%s\n" % records_name

            if smr_result in ["not_done"]:
                pass
            else:
                requester_schema += "AFB, %s\n" % smr_result.upper().replace("_", " ")

            if lab_xpert_mtb_rif_assay_result in ["not_done", "error_invalid"]:
                pass
            else:
                requester_schema += "XPERT, %s%s%s\n" % (lab_xpert_mtb_rif_assay_result.upper().replace("_", " "), "" if not lab_xpert_mtb_rif_assay_grades else " (%s)" % lab_xpert_mtb_rif_assay_grades.upper().replace("_", " "), "" if lab_xpert_mtb_rif_assay_rif_result in ["not_done", "error_invalid"] else ", RIF RESISTANCE %s" % lab_xpert_mtb_rif_assay_rif_result.upper().replace("_", " "))
            
            if lab_urine_lf_lam_result in ["not_done", "error_invalid"]:
                pass
            else:
                requester_schema += "URINE, %s\n" % lab_urine_lf_lam_result.upper().replace("_", " ")

            requester_schema += "INFO %s" % info_line

            return requester_schema

        except Exception as error:
            raise InternalServerError(error)

    def __client_schema__(self) -> str:
        """
        """
        try:
            client_schema = "The results for the test you made are available at the TB Lab. Call 670656041 if you have any questions."

            return client_schema

        except Exception as error:
            raise InternalServerError(error)

    def __send_sms_message__(self, text: str, contacts: list) -> None:
        """
        """
        sms_url = f"{self.openapi_url}/v1/sms"
        operator_url = f"{self.openapi_url}/v1/sms/operators"
        auth_id = self.auth_id

        payload = []

        for contact in contacts:
            payload.append({
                "operator_name":"",
                "text":text.strip()[:149],
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


