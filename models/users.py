import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError
from peewee import IntegrityError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from models.sites import Site_Model

from datetime import datetime

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Forbidden

class User_Model:
    """
    """
    def __init__(self) -> None:
        """
        """
        self.Users = Users
        self.Users_sites = Users_sites
        self.Data = Data
        self.Sites = Site_Model

    def create(self, email: str, password: str, phone_number: str, name: str, occupation: str, site_id: int, sms_notifications_type: str) -> str:
        """
        Add user to database.

        Arguments:
            email: str,
            password: str,
            phone_number: str,
            name: str,
            occupation: str,
            site_id: int,
            sms_notifications_type: str

        Returns:
            str
        """
        try:
            try:
                self.Users.get(self.Users.email == email)
            except self.Users.DoesNotExist:
                logger.debug("creating user record for '%s' ..." % email)

                data = self.Data()
                password_hash = data.hash(password)

                user = self.Users.create(
                    email= email,
                    password_hash= password_hash,
                    phone_number= data.encrypt(phone_number)["e_data"],
                    name= data.encrypt(name)["e_data"],
                    occupation= data.encrypt(occupation)["e_data"],
                    sms_notifications_type = sms_notifications_type,
                    iv = data.iv
                )

                logger.debug("adding user '%s' to site '%d' ..." % (email, site_id))
                self.Users_sites.create(
                    user_id=user.id,
                    site_id=site_id
                )

                logger.info("- User '%s' successfully created" % email)
                return str(user)
            else:
                logger.error("user '%s' already has a record" % email)
                raise Conflict()

        except DatabaseError as err:
            logger.error("creating user '%s' failed check logs" % email)
            raise InternalServerError(err) from None

    def authenticate(self, email: str, password: str, admin: bool = False) -> dict:
        """
        Find user in database by email and password.

        Arguments:
            email: str,
            password: str

        Returns:
            dict
        """
        try:
            logger.debug("authenticating user %s ..." % email)

            data = self.Data()

            hash_password = data.hash(password)
            
            try:
                user = self.Users.get(
                    self.Users.email == email,
                    self.Users.password_hash == hash_password,
                    self.Users.account_status == "approved"
                    )
            except self.Users.DoesNotExist:
                logger.error("No user found")
                raise Unauthorized()
            else:
                if admin:
                    self.check_permission(user_id=user.id, scope=["admin", "super_admin"])

                result = self.fetch_user(user_id=user.id, account_status="approved")

                logger.info("- User %s successfully verified" % email)
                return result
        
        except DatabaseError as err:
            logger.error("verifying user %s failed check logs" % email)
            raise InternalServerError(err) from None

    def fetch_user(self, user_id: int, account_status: str = None, no_sites: bool = False) -> dict:
        """
        Find a single user.

        Arguments:
            user_id: int,
            no_sites: bool,
            account_status: str
        
        Returns:
            dict
        """
        try:
            logger.debug("finding user %s ..." % user_id)
            
            result = []
            
            data = self.Data()

            if not account_status:
                users = (
                    self.Users.select()
                    .where(self.Users.id == user_id)
                    .dicts()
                )
            else:
                users = (
                    self.Users.select()
                    .where(self.Users.id == user_id, self.Users.account_status == account_status)
                    .dicts()
                )

            for user in users:
                iv = user["iv"]

                if no_sites:
                    result.append({
                        "id": user["id"],
                        "email": user["email"],
                        "name": data.decrypt(user["name"], iv),
                        "phone_number": data.decrypt(user["phone_number"], iv),
                        "occupation": data.decrypt(user["occupation"], iv),
                        "account_status": user["account_status"],
                        "account_type": user["account_type"],
                        "account_request_date": user["account_request_date"],
                        "account_approved_date": user["account_approved_date"],
                        "permitted_export_types": user["permitted_export_types"],
                        "permitted_export_range": user["permitted_export_range"],
                        "permitted_decrypted_data": user["permitted_decrypted_data"],
                        "permitted_approve_accounts": user["permitted_approve_accounts"],
                        "sms_notifications": user["sms_notifications"],
                        "sms_notifications_type": user["sms_notifications_type"]
                    })
                else:
                    logger.debug("Fetching all sites for user '%s' ..." % user["id"])

                    site_arr = []

                    user_sites = self.Users_sites.select(
                        self.Users_sites.site_id
                        ).where(
                            self.Users_sites.user_id == user["id"]
                            ).dicts()
                    
                    Sites = self.Sites()

                    for user_site in user_sites.iterator():
                        site = Sites.fetch_site(site_id=user_site["site_id"])
                        region = Sites.fetch_region(region_id=site["region_id"])
                        site_arr.append({
                            "id": site["id"],
                            "name": site["name"],
                            "site_code": site["site_code"],
                            "region": {
                                "id": region["id"],
                                "name": region["name"]
                            }
                        })

                    result.append({
                        "id": user["id"],
                        "email": user["email"],
                        "name": data.decrypt(user["name"], iv),
                        "phone_number": data.decrypt(user["phone_number"], iv),
                        "occupation": data.decrypt(user["occupation"], iv),
                        "account_status": user["account_status"],
                        "account_type": user["account_type"],
                        "account_request_date": user["account_request_date"],
                        "account_approved_date": user["account_approved_date"],
                        "permitted_export_types": user["permitted_export_types"],
                        "permitted_export_range": user["permitted_export_range"],
                        "permitted_decrypted_data": user["permitted_decrypted_data"],
                        "permitted_approve_accounts": user["permitted_approve_accounts"],
                        "sms_notifications": user["sms_notifications"],
                        "sms_notifications_type": user["sms_notifications_type"],
                        "users_sites": site_arr
                    })

            # check for duplicates
            if len(result) > 1:
                logger.error("Multiple users %s found" % user_id)
                raise Conflict()

            # check for no user
            if len(result) < 1:
                logger.error("No user found")
                raise Unauthorized()

            logger.info("- User %s found" % user_id)

            return result[0]

        except DatabaseError as err:
            logger.error("failed to find user %s check logs" % user_id)
            raise InternalServerError(err) from None

    def fetch_users(self, account_status: str = None, no_sites: bool = False) -> list:
        """
        Fetch all users.

        Arguments:
            account_status: str,
            no_sites: bool

        Returns:
            list
        """
        try:
            logger.debug("fetching all user records ...")
            
            result = []

            data = self.Data()
            
            if account_status:
                if not account_status in ["pending"]:
                    logger.error("invalid account_status '%s'" % account_status)
                    raise Unauthorized()       
                else:          
                    users = self.Users.select().where(
                        self.Users.account_status == account_status
                        ).dicts()
            else:
                users = self.Users.select().dicts()

            for user in users.iterator():
                iv = user["iv"]

                if no_sites:
                    result.append({
                        "id": user["id"],
                        "email": user["email"],
                        "name": data.decrypt(user["name"], iv),
                        "phone_number": data.decrypt(user["phone_number"], iv),
                        "occupation": data.decrypt(user["occupation"], iv),
                        "account_status": user["account_status"],
                        "account_type": user["account_type"],
                        "account_request_date": user["account_request_date"],
                        "account_approved_date": user["account_approved_date"],
                        "permitted_export_types": user["permitted_export_types"],
                        "permitted_export_range": user["permitted_export_range"],
                        "permitted_decrypted_data": user["permitted_decrypted_data"],
                        "permitted_approve_accounts": user["permitted_approve_accounts"],
                        "sms_notifications": user["sms_notifications"],
                        "sms_notifications_type": user["sms_notifications_type"]
                    })
                else:
                    logger.debug("Fetching all sites for user '%s' ..." % user["id"])
                    
                    site_arr = []

                    user_sites = self.Users_sites.select(
                        self.Users_sites.site_id
                        ).where(
                            self.Users_sites.user_id == user["id"]
                            ).dicts()

                    Sites = self.Sites()

                    # populate user_sites from Users_sites table
                    for user_site in user_sites.iterator():
                        site = Sites.fetch_site(site_id=user_site["site_id"])
                        region = Sites.fetch_region(region_id=site["region_id"])
                        site_arr.append({
                            "id": site["id"],
                            "name": site["name"],
                            "site_code": site["site_code"],
                            "region": {
                                "id": region["id"],
                                "name": region["name"]
                            }
                        })

                    result.append({
                        "id": user["id"],
                        "email": user["email"],
                        "name": data.decrypt(user["name"], iv),
                        "phone_number": data.decrypt(user["phone_number"], iv),
                        "occupation": data.decrypt(user["occupation"], iv),
                        "account_status": user["account_status"],
                        "account_type": user["account_type"],
                        "account_request_date": user["account_request_date"],
                        "account_approved_date": user["account_approved_date"],
                        "permitted_export_types": user["permitted_export_types"],
                        "permitted_export_range": user["permitted_export_range"],
                        "permitted_decrypted_data": user["permitted_decrypted_data"],
                        "permitted_approve_accounts": user["permitted_approve_accounts"],
                        "sms_notifications": user["sms_notifications"],
                        "sms_notifications_type": user["sms_notifications_type"],
                        "users_sites": site_arr
                    })

                logger.info("- Successfully fetched all users")

            return result

        except DatabaseError as err:
            logger.error("failed to fetch all users check logs")
            raise InternalServerError(err) from None

    def update(self, id: int, account_status: str, permitted_export_types: str, account_type: str, permitted_export_range: int, permitted_approve_accounts: bool, permitted_decrypted_data: bool) -> int:
        """
        Update a user's account.

        Arguments:
            id: int,
            account_status: str,
            permitted_export_types: str,
            account_type: str,
            permitted_export_range: str,
            permitted_approve_accounts: bool,
            permitted_decrypted_data: bool

        Returns:
            int
        """
        try:
            if not account_status in ["pending", "approved", "suspended"]:
                logger.error("invalid account_status '%s'" % account_status)
                raise Unauthorized()               

            logger.debug("Updating user %d record ..." % id)
            
            user = self.Users.update(account_status=account_status, permitted_export_types=permitted_export_types, account_type=account_type, permitted_export_range=permitted_export_range, permitted_approve_accounts=permitted_approve_accounts, permitted_decrypted_data=permitted_decrypted_data).where(self.Users.id == id)

            user.execute()

            logger.info("- Successfully updated user %s" % id)
            return id

        except DatabaseError as err:
            logger.error("failed to update users %d check logs" % id)
            raise InternalServerError(err) from None

    def update_account_status(self, user_id: int, account_status: str) -> bool:
        """
        """
        try:
            logger.debug("Verifying account_status %s ..." % account_status)

            if not account_status in ["pending", "approved", "suspended"]:
                logger.error("invalid account_status '%s'" % account_status)
                raise Unauthorized()        
            
            self.fetch_user(user_id=user_id, no_sites=True)

            logger.debug("updating account_status %s for user %s ..." % (account_status, user_id))

            if account_status == "approved":
                upd_account_status = self.Users.update(
                    account_status=account_status,
                    account_approved_date=datetime.now()
                    ).where(
                        self.Users.id == user_id
                    )
            else:
                upd_account_status = self.Users.update(
                    account_status=account_status
                    ).where(
                        self.Users.id == user_id
                    )
            
            upd_account_status.execute()

            logger.info("- Successfully updated_account_status for user %s" % user_id)
            return True
        except DatabaseError as err:
            logger.error("Failed to updated_account_status for user %s check logs" % user_id)
            raise InternalServerError(err) from None

    def check_permission(self, user_id: int, scope: list, permitted_approve_accounts: bool = False) -> str:
        """
        Check a user's scope.

        Arguments:
            user_id: int,
            scope: list
        
        Returns:
            str
        """
        try:
            logger.debug("checking permissions for user %s ..." % user_id)

            try:
                user = self.Users.get(self.Users.id == user_id, self.Users.account_status == "approved")
            except self.Users.DoesNotExist:
                logger.error("no user found")
                raise Unauthorized()
            else:
                if not user.account_type in scope:
                    logger.error("account_type = %s is not allowed to access the request resource" % user.account_type)
                    raise Forbidden()
                else:
                    if permitted_approve_accounts:
                        if not user.permitted_approve_accounts:
                            logger.error("not permitted to change account_status")
                            raise Forbidden()
                    else:
                        return user.account_type

        except DatabaseError as err:
            logger.error("failed to find user %s check logs" % user_id)
            raise InternalServerError(err) from None

    def add_site(self, users_sites: list, user_id: int) -> None:
        """
        Add a user's sites.

        Arguments:
            users_sites: list

        Returns:
            None
        """
        try:
            for site_id in users_sites:
                try:
                    self.Users_sites.create(user_id=user_id, site_id=site_id)
                    logger.info("- Successfully added site_id=%s to user_id=%s" % (site_id, user_id))
                except IntegrityError as error:
                    logger.error(error)

        except DatabaseError as err:
            logger.error("creating users_sites failed check logs")
            raise InternalServerError(err) from None

    def remove_site(self, users_sites: list, user_id: int) -> None:
        """
        Remove a user's sites.

        Arguments:
            users_sites: list

        Returns:
            None
        """
        try:
            for site_id in users_sites:
                try:
                    user_site = self.Users_sites.get(user_id=user_id, site_id=site_id)
                except self.Users_sites.DoesNotExist:
                    logger.error("no record for user_id=%s and site_id=%s. Nothing to delete" % (user_id, site_id))
                else:
                    user_site.delete_instance()
                    logger.info("- Sucessfully removed site_id=%s from user_id=%s" % (site_id, user_id))

        except DatabaseError as err:
            logger.error("removing users_sites failed check logs")
            raise InternalServerError(err) from None

    def update_profile(self, id: int, phone_number: str, name: str, occupation: str, sms_notifications: bool, sms_notifications_type: str) -> int:
        """
        Update a user's profile information.

        Arguments:
            id: int,
            phone_number: str,
            name: str,
            occupation: str,
            sms_notifications: bool,
            sms_notifications_type: str

        Returns:
            int
        """
        try:
            logger.debug("Updating user %d record ..." % id)

            data = self.Data()
            
            user = self.Users.update(
                phone_number=data.encrypt(phone_number)["e_data"],
                name=data.encrypt(name)["e_data"],
                occupation=data.encrypt(occupation)["e_data"],
                sms_notifications=sms_notifications,
                sms_notifications_type=sms_notifications_type,
                iv=data.iv
            ).where(self.Users.id == id)

            user.execute()

            logger.info("- Successfully updated user %s" % id)
            return id

        except DatabaseError as err:
            logger.error("failed to update user %d. Check logs" % id)
            raise InternalServerError(err) from None

    def update_password(self, id: int, current_password: str, new_password: str) -> int:
        """
        Update a user's password.

        Arguments:
            id: int,
            current_password: str,
            new_password: str

        Returns:
            int
        """
        try:
            user = self.Users.select(
                self.Users.password_hash
            ).where(
                self.Users.id == id
                ).dicts()

            password = user[0]["password_hash"]

            logger.debug("Updating user %d password ..." % id)

            data = self.Data()

            if password != data.hash(current_password):
                logger.error("Wrong password")
                raise Forbidden()
            
            upd_user = self.Users.update(
                password_hash=data.hash(new_password)
            ).where(self.Users.id == id)

            upd_user.execute()

            logger.info("- Successfully updated user %s password" % id)
            return id

        except DatabaseError as err:
            logger.error("failed to update user %d  password. Check logs" % id)
            raise InternalServerError(err) from None

    def check_account_status(self, user_id: int) -> bool:
        """
        """
        try:
            logger.debug("checking account status for user %s ..." % user_id)

            try:
                self.Users.get(self.Users.id == user_id, self.Users.account_status == "approved")
            except self.Users.DoesNotExist:
                logger.error("Unapproved account")
                raise Unauthorized()
            else:
                logger.info("Approved account")
                return True

        except DatabaseError as err:
            logger.error("failed to check account status for user %d. Check logs" % user_id)
            raise InternalServerError(err) from None