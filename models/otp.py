import logging
logger = logging.getLogger(__name__)

import requests

# configurations
from Configs import baseConfig
config = baseConfig()
smswithoutborders = config["SMSWITHOUTBORDERS"]

from peewee import DatabaseError

from schemas.users.users_otp import Users_otp

from datetime import datetime

from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import InternalServerError

class OTP_Model:
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
        self.Users_otp = Users_otp

    def create(self, phone_number: str) -> dict:
        """
        """
        try:
            otp = self.Users_otp.create(
                phone_number=phone_number
            )

            logger.info("- Successfully created user_otp for %s" % phone_number)

            text = self.__schema__(code=otp.code)
            contacts = []
            contacts.append(phone_number)

            return {
                "id": otp.id,
                "text": text,
                "contacts": contacts
            }

        except DatabaseError as err:
            logger.error("creating user_otp '%s' failed check logs" % phone_number)
            raise InternalServerError(err)

    def check(self, otp_id:int, phone_number:str, code:int) -> None:
        """
        """
        try:
            try:
                otp = self.Users_otp.get(
                    self.Users_otp.id == otp_id,
                    self.Users_otp.phone_number == phone_number,
                    self.Users_otp.status == "pending"
                )
            except self.Users_otp.DoesNotExist:
                logger.error("OTP record '%d' not found ..." % otp_id)
                raise Forbidden()

            else:
                if otp.code != int(code):
                    logger.error("Invalid code")
                    raise Forbidden()

                age = otp.expires.timestamp() - datetime.now().timestamp()

                if age <= 0:
                    otp_expire = self.Users_otp.update(
                        status = "expired"
                    ).where(
                        self.Users_otp.id == otp_id,
                        self.Users_otp.phone_number == phone_number,
                        self.Users_otp.status == "pending"
                    )

                    otp_expire.execute()

                    logger.error("Expired code")
                    raise Forbidden()


                otp_approved = self.Users_otp.update(
                    status = "approved"
                ).where(
                    self.Users_otp.id == otp_id,
                    self.Users_otp.phone_number == phone_number,
                    self.Users_otp.status == "pending"
                )

                otp_approved.execute()

                logger.info("- Successfully validated OTP '%d'" % otp_id)

        except DatabaseError as err:
            logger.error("Validating user_otp '%s' failed check logs" % phone_number)
            raise InternalServerError(err)
    
    def __schema__(self, code: int):
        """
        """
        try:
            schema = "Your CHPR-IS verification code is: %d" % code

            return schema

        except Exception as error:
            raise InternalServerError(error)

    def __send__(self, text: str, contacts: list):
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


