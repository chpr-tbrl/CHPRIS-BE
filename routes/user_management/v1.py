import logging
import json
import werkzeug

logger = logging.getLogger(__name__)

from Configs import configuration
from error import BadRequest, InternalServerError, Unauthorized, Conflict
from flask import Blueprint, request, jsonify
from security import Cookie
from datetime import timedelta
from schemas import users_db, sites_db

v1 = Blueprint("v1", __name__)
config = configuration()
api = config["API"]
cookie_name = api['COOKIE_NAME']

from models import (
    verify_user,
    create_session,
    create_user,
    change_state,
    get_all_users,
    find_session,
    update_session
)

@v1.after_request
def after_request(response):
    users_db.close()
    sites_db.close()
    return response

@v1.route("/signup", methods=["POST"])
def signup():
    try:
        if not "email" in request.json or not request.json["email"]:
            logger.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            logger.error("no password")
            raise BadRequest()
        elif not "phone_number" in request.json or not request.json["phone_number"]:
            logger.error("no phone_number")
            raise BadRequest()
        elif not "name" in request.json or not request.json["name"]:
            logger.error("no name")
            raise BadRequest()
        elif not "occupation" in request.json or not request.json["occupation"]:
            logger.error("no occupation")
            raise BadRequest()
        elif not "site" in request.json or not request.json["site"]:
            logger.error("no site")
            raise BadRequest()
        elif not "region" in request.json or not request.json["region"]:
            logger.error("no region")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        phone_number = request.json["phone_number"]
        name = request.json["name"]
        site = request.json["site"]
        region = request.json["region"]
        occupation = request.json["occupation"]

        user = create_user(
            email, 
            password, 
            phone_number,
            name,
            region,
            occupation,
            site 
        )
        change_state(user, "verified")

        res = jsonify(user)

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
        cookie_data = json.dumps({"sid": session["sid"], "uid": session["uid"], "cookie": session["data"]})
        e_cookie = cookie.encrypt(cookie_data)
        res.set_cookie(
            cookie_name,
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

@v1.route("/users", methods=["GET"])
def getAllUsers():
    try:
        if not request.cookies.get(cookie_name):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        cookie = Cookie()
        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = json_cookie["uid"]
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        user_id = find_session(sid, uid, user_agent, user_cookie)
        users_list = get_all_users()
        session = update_session(sid, user_id)

        res = jsonify(users_list)
        cookie = Cookie()
        cookie_data = json.dumps({"sid": session["sid"], "uid": session["uid"], "cookie": session["data"]})
        e_cookie = cookie.encrypt(cookie_data)
        res.set_cookie(
            cookie_name,
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