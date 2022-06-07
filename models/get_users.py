import logging

logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from werkzeug.exceptions import InternalServerError

def get_all_users() -> list:
    """
    Fetch all users.

    Arguments:
        None

    Returns:
        list
    """
    try:
        logger.debug("fetching all user records ...")
        result = []
        
        users = Users.select().dicts()

        for user in users.iterator():
            logger.debug("Fetching all sites for user '%s' ..." % user["id"])
            sites = Users_sites.select(Users_sites.site_id).where(Users_sites.user_id == user["id"]).dicts()
            site_arr = []

            for site in sites.iterator():
                site_arr.append(site["site_id"])

            result.append({
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

        logger.info("- Successfully fetched all users")
        return result

    except DatabaseError as err:
        logger.error("failed to fetch all users check logs")
        raise InternalServerError(err) from None
