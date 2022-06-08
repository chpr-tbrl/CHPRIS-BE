import logging
logger = logging.getLogger(__name__)

from peewee import DatabaseError

from schemas.users.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Forbidden

def check_permission(user_id: int, scope: list, permitted_approve_accounts: bool = False) -> str:
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
            user = Users.get(Users.id == user_id, Users.account_status == "approved")
        except Users.DoesNotExist:
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
