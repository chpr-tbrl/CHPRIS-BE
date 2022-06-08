import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized

def update_user(id: int, account_status: str, permitted_export_types: str, account_type: str, permitted_export_range: int, permitted_approve_accounts: bool, permitted_decrypted_data: bool) -> int:
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
        
        user = Users.update(account_status=account_status, permitted_export_types=permitted_export_types, account_type=account_type, permitted_export_range=permitted_export_range, permitted_approve_accounts=permitted_approve_accounts, permitted_decrypted_data=permitted_decrypted_data).where(Users.id == id)
        user.execute()

        logger.info("- Successfully updated user %s" % id)
        return id

    except DatabaseError as err:
        logger.error("failed to update users %d check logs" % id)
        raise InternalServerError(err) from None
