import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites
from schemas.records.records import Records

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

class Contact_Model:
    """
    """
    def __init__(self) -> None:
        """
        """
        self.Users = Users
        self.Users_sites = Users_sites
        self.Records = Records
        self.Data = Data

    def lab(self, record_id: int, sms_notification_type: str) -> list:
        """
        """
        try:
            try:
                record = self.Records.get(self.Records.record_id == record_id)
            except self.Records.DoesNotExist:
                logger.error("Record: %d not found." % record_id)
                raise Unauthorized()
            else:
                logger.debug("finding users that belong to site_id: %d with sms_notification_type: %s ..." % (record.site_id, sms_notification_type))
                
                result = []
                
                data = self.Data()

                notification_type = sms_notification_type.split(",")

                if len(notification_type) == 2:
                    users = (
                        self.Users.select(
                            self.Users.phone_number,
                            self.Users.iv
                        )
                        .where(self.Users.account_status == "approved", self.Users.sms_notifications == True, (self.Users.sms_notifications_type == notification_type[0] | self.Users.sms_notifications_type == notification_type[1]))
                        .join(self.Users_sites)
                        .where(self.Users_sites.site_id == record.site_id)
                        .dicts()
                    )
                elif len(notification_type) == 1:
                    users = (
                        self.Users.select(
                            self.Users.phone_number,
                            self.Users.iv
                        )
                        .where(self.Users.account_status == "approved", self.Users.sms_notifications == True, self.Users.sms_notifications_type == notification_type[0])
                        .join(self.Users_sites)
                        .where(self.Users_sites.site_id == record.site_id)
                        .dicts()
                    )

                for user in users:
                    iv = user["iv"]

                    result.append(data.decrypt(user["phone_number"], iv))

                logger.info("- Succesfully gathered lab contacts")
                return result

        except DatabaseError as err:
            logger.error("Failed to find users that belong to site_id: %d with sms_notification_type: %s. Check logs." % (record.site_id, sms_notification_type))
            raise InternalServerError(err) from None