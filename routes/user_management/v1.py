import logging
import json
import werkzeug

logger = logging.getLogger(__name__)

from Configs import configuration
from error import BadRequest, InternalServerError, Unauthorized, Conflict
from flask import Blueprint, request, jsonify
from security import Cookie
from datetime import timedelta

v1 = Blueprint("v1", __name__)
config = configuration()
api = config["API"]

from models import (
    verify_user,
    create_session
)

@v1.route("/login", methods=["POST"])
def login():
    try:
        if not "email" in request.json or not request.json["email"]:
            logger.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            logger.error("no password")
            raise BadRequest()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        user_agent = request.headers.get("User-Agent")

        user = verify_user(email, password)
        session = create_session(user["uid"], user_agent)

        res = jsonify(user)

        cookie = Cookie()
        cookie_data = json.dumps({"sid": session["sid"], "cookie": session["data"]})
        e_cookie = cookie.encrypt(cookie_data)
        res.set_cookie(
            api['COOKIE_NAME'],
            e_cookie,
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Conflict as err:
        return str(err), 409
    except InternalServerError as err:
        logger.error(err)
        return "internal server error", 500
    except Exception as err:
        logger.error(err)
        return "internal server error", 500