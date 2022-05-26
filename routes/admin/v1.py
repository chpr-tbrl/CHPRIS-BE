import logging

logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]
cookie_name = api['COOKIE_NAME']

from flask import Blueprint, request, jsonify
v1 = Blueprint("admin_v1", __name__)

from security.cookie import Cookie
from datetime import timedelta

from schemas.users.baseModel import users_db
from schemas.sites.baseModel import sites_db
from schemas.records.baseModel import records_db

from models.get_users import get_all_users
from models.find_users import find_user
from models.update_users import update_user

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Forbidden

@v1.after_request
def after_request(response):
    users_db.close()
    sites_db.close()
    records_db.close()
    return response

@v1.route("/users", methods=["GET"])
def getAllUsers():
    """
    Fetch all users.

    Body:
       None

    Response:
        200: list
        400: str
        401: str
        409: str
        403: str
        500: str
    """
    try:
        # if not request.cookies.get(cookie_name):
        #     logger.error("no cookie")
        #     raise Unauthorized()
        # elif not request.headers.get("User-Agent"):
        #     logger.error("no user agent")
        #     raise BadRequest()

        # cookie = Cookie()
        # e_cookie = request.cookies.get(cookie_name)
        # d_cookie = cookie.decrypt(e_cookie)
        # json_cookie = json.loads(d_cookie)

        # sid = json_cookie["sid"]
        # uid = json_cookie["uid"]
        # user_cookie = json_cookie["cookie"]
        # user_agent = request.headers.get("User-Agent")

        # user_id = find_session(sid, uid, user_agent, user_cookie)
        users_list = get_all_users()
        # session = update_session(sid, user_id)

        res = jsonify(users_list)
        # cookie = Cookie()
        # cookie_data = json.dumps({"sid": session["sid"], "uid": session["uid"], "cookie": session["data"]})
        # e_cookie = cookie.encrypt(cookie_data)
        # res.set_cookie(
        #     cookie_name,
        #     e_cookie,
        #     max_age=timedelta(milliseconds=session["data"]["maxAge"]),
        #     secure=session["data"]["secure"],
        #     httponly=session["data"]["httpOnly"],
        #     samesite=session["data"]["sameSite"],
        # )

        return res, 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Forbidden as err:
        return str(err), 403

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>", methods=["PUT"])
def updateUser(user_id):
    """
    Update a user's account.

    Body:
        occupation: str,
        phone_number: str,
        region_id: int,
        site_id: int,
        state: str,
        type_of_export: str,
        type_of_user: str

    Response:
        200: str
        400: str
        401: str
        409: str
        403: str
        500: str
    """
    try:
        user = find_user(user_id=user_id)

        payload = (
            user["id"],
            request.json["occupation"],
            request.json["phone_number"],
            request.json["region_id"],
            request.json["site_id"],
            request.json["state"],
            request.json["type_of_export"],
            request.json["type_of_user"]
        )

        result = update_user(*payload)

        return result, 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Forbidden as err:
        return str(err), 403

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500