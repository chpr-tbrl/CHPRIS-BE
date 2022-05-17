import logging
from error import InternalServerError
from Configs import configuration

config = configuration()

api = config["API"]

import peewee as pw
from schemas.users.users import Users

logger = logging.getLogger(__name__)

def get_all_users():
    try:
        logger.debug(f"fetching all user records ...")
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
                "region": user["region"],
                "site": user["site"],
                "state": user["state"]
            })

        logger.info("Successfully fetched all users")
        return result
    except (pw.DatabaseError) as err:
        logger.error(f"failed to fetch all users check logs")
        raise InternalServerError(err)
