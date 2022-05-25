import logging
logger = logging.getLogger(__name__)

from error import InternalServerError

from peewee import DatabaseError
from schemas.users.users import Users

def get_all_users():
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
        
        users = (
            Users.select()
            .dicts()
        )
        for user in users:
            result.append({
                "createdAt": user["createdAt"],
                "email": user["email"],
                "id": user["id"],
                "name": user["name"],
                "occupation": user["occupation"],
                "phone_number": user["phone_number"],
                "type_of_user": user["type_of_user"],
                "type_of_export": user["type_of_export"],
                "region_id": user["region_id"],
                "site_id": user["site_id"],
                "state": user["state"]
            })

        logger.info("- Successfully fetched all users")
        return result
    except DatabaseError as err:
        logger.error("failed to fetch all users check logs")
        raise InternalServerError(err)
