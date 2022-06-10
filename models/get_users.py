import logging
from security import data

logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from models.find_sites import find_site
from models.find_regions import find_region

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

def get_all_users(account_status: str = None) -> list:
    """
    Fetch all users.

    Arguments:
        account_status: str

    Returns:
        list
    """
    try:
        logger.debug("fetching all user records ...")
        result = []
        
        if account_status:
            if not account_status in ["pending"]:
                logger.error("invalid account_status '%s'" % account_status)
                raise Unauthorized()       
            else:          
                users = Users.select().where(Users.account_status == account_status).dicts()
        else:
            users = Users.select().dicts()

        for user in users.iterator():
            logger.debug("Fetching all sites for user '%s' ..." % user["id"])
            user_sites = Users_sites.select(Users_sites.site_id).where(Users_sites.user_id == user["id"]).dicts()
            site_arr = []

            # populate user_sites from Users_sites table
            for user_site in user_sites.iterator():
                site = find_site(site_id=user_site["site_id"])
                region = find_region(region_id=site["region_id"])
                site_arr.append({
                    "id": site["id"],
                    "name": site["name"],
                    "region": {
                        "id": region["id"],
                        "name": region["name"]
                    }
                })

            iv = user["iv"]
            data = Data()
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
                "users_sites": site_arr
            })

        logger.info("- Successfully fetched all users")
        return result

    except DatabaseError as err:
        logger.error("failed to fetch all users check logs")
        raise InternalServerError(err) from None
