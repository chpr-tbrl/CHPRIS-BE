import logging
from error import InternalServerError, Conflict
from Configs import configuration
from security import Data

config = configuration()

api = config["API"]

import peewee as pw
from schemas import Users

logger = logging.getLogger(__name__)

def create_user(email, password, phone_number, name, region, occupation, site):
    try:
        logger.debug(f"creating user record for {email} ...")
        
        data = Data()
        password_hash = data.hash(password)

        user = Users.create(
            email=email,
            password=password_hash,
            phone_number=phone_number,
            name=name,
            region=region,
            occupation=occupation,
            site=site
        )
        logger.info(f"User {email} successfully created")
        return str(user)
    except pw.IntegrityError as err:
        logger.error(f"user {email} already has a record")
        raise Conflict()
    except (pw.DatabaseError) as err:
        logger.error(f"creating user {email} failed check logs")
        raise InternalServerError(err)
