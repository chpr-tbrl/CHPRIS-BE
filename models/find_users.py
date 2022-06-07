import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from models.find_sites import find_site
from models.find_regions import find_region

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def find_user(user_id: int) -> dict:
    """
    Find a user.

    Arguments:
        user_id: int
    
    Returns:
        dict
    """
    try:
        logger.debug("finding user %s ..." % user_id)
        
        users = (
            Users.select()
            .where(Users.id == user_id, Users.account_status == "approved")
            .dicts()
        )

        result = []
        for user in users:
            logger.debug("Fetching all sites for user '%s' ..." % user["id"])
            user_sites = Users_sites.select(Users_sites.site_id).where(Users_sites.user_id == user["id"]).dicts()
            site_arr = []

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

            result.append({
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "phone_number": user["phone_number"],
                "occupation": user["occupation"],
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
