import logging

logger = logging.getLogger(__name__)

from error import BadRequest, InternalServerError
from flask import Blueprint, request

v1 = Blueprint("v1", __name__)

@v1.route("/login", methods=["POST"])
def login():
    try:

        return
    except BadRequest as error:
        return str(error), 400
    except InternalServerError as error:
        logger.error(error)
        return "internal server error", 500
    except Exception as error:
        logger.error(error)
        return "internal server error", 500
