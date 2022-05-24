import logging
logger = logging.getLogger(__name__)

from error import InternalServerError

from peewee import DatabaseError
from schemas.users.users import Users

def get_all_users():
    """
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
                "last_login": user["last_login"],
                "name": user["name"],
                "occupation": user["occupation"],
                "phone_number": user["phone_number"],
                "type_of_user": user["type_of_user"],
                "type_of_export": user["type_of_export"],
                "region": user["region"],
                "site": user["site"],
                "state": user["state"]
            })

        logger.info("- Successfully fetched all users")
        return result
    except DatabaseError as err:
        logger.error("failed to fetch all users check logs")
        raise InternalServerError(err)
