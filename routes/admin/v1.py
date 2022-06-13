import logging

logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]
cookie_name = api['COOKIE_NAME']

import json

from flask import Blueprint, request, jsonify
v1 = Blueprint("admin_v1", __name__)

from security.cookie import Cookie
from datetime import timedelta

from schemas.users.baseModel import users_db
from schemas.sites.baseModel import sites_db
from schemas.records.baseModel import records_db

from models.find_sessions import find_session
from models.update_sessions import update_session
from models.check_permissions import check_permission
from models.get_users import get_all_users
from models.find_users import find_user
from models.update_users import update_user
from models.create_regions import create_region
from models.create_sites import create_site
from models.change_account_status import update_account_status
from models.add_users_sites import add_user_site
from models.remove_users_sites import remove_user_site

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
def getAllUsers() -> list:
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
        
        # check permission
        check_permission(user_id=user_id, scope=["admin", "super_admin"])
    
        account_status = request.args.get("account_status")

        users_list = get_all_users(account_status=account_status)

        res = jsonify(users_list)

        session = update_session(sid, user_id)
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

@v1.route("/users/<int:user_id>", methods=["POST","PUT"])
def updateUser(user_id: int) -> None:
    """
    Update a user's account.
    
    Parameters:
        user_id: int

    Body:
        account_status: str,
        permitted_export_types: list,
        account_type: str,
        permitted_export_range: int,

    Response:
        200: None
        400: str
        401: str
        409: str
        403: str
        500: str
    """
    try:
        # update account
        if request.method == "PUT":
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

            admin_user_id = find_session(sid, uid, user_agent, user_cookie) 
            
            # check permission
            account_type = check_permission(user_id=admin_user_id, scope=["admin", "super_admin"])
            
            user = find_user(user_id=user_id, no_sites=True, update=True)

            if user["account_type"] == "super_admin" and account_type == "admin":
                logger.error("'%s' cannot update '%s' account_type" % (account_type, user["account_type"]))
                raise Forbidden()
            elif user["account_type"] == "admin" and account_type == "admin":
                logger.error("'%s' cannot update '%s' account_type" % (account_type, user["account_type"]))
                raise Forbidden()

            payload = (
                user["id"],
                request.json["account_status"],
                request.json["permitted_export_types"],
                request.json["account_type"],
                request.json["permitted_export_range"],
                request.json["permitted_approve_accounts"],
                request.json["permitted_decrypted_data"]
            )

            update_user(*payload)

            res = jsonify()

            session = update_session(sid, admin_user_id)
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

        # change account_status
        elif request.method == "POST":
            if not request.cookies.get(cookie_name):
                logger.error("no cookie")
                raise Unauthorized()
            elif not request.headers.get("User-Agent"):
                logger.error("no user agent")
                raise BadRequest()
            elif not "account_status" in request.json or not request.json["account_status"]:
                logger.error("no account_status")
                raise BadRequest()

            cookie = Cookie()
            e_cookie = request.cookies.get(cookie_name)
            d_cookie = cookie.decrypt(e_cookie)
            json_cookie = json.loads(d_cookie)

            sid = json_cookie["sid"]
            uid = json_cookie["uid"]
            user_cookie = json_cookie["cookie"]
            user_agent = request.headers.get("User-Agent")

            admin_user_id = find_session(sid, uid, user_agent, user_cookie) 
            
            # check permission
            check_permission(user_id=admin_user_id, scope=["admin", "super_admin"], permitted_approve_accounts=True)

            account_status = request.json["account_status"]

            update_account_status(user_id=user_id, account_status=account_status)

            res = jsonify()

            session = update_session(sid, admin_user_id)
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

@v1.route("/users/<int:user_id>/sites", methods=["POST", "DELETE"])
def addUserSites(user_id: int) -> None:
    """
    Add a user's sites.
    
    Parameters:
        user_id: int

    Body:
       []

    Response:
        200: None
        400: str
        401: str
        409: str
        403: str
        500: str
    """
    try:
        if not request.cookies.get(cookie_name):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()
        elif not isinstance(request.json, list):
            logger.error("no request body must be an array")
            raise BadRequest()
    
        cookie = Cookie()
        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = json_cookie["uid"]
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        admin_user_id = find_session(sid, uid, user_agent, user_cookie) 
        
        # check permission
        check_permission(user_id=admin_user_id, scope=["admin", "super_admin"])

        user_sites = request.json

        if request.method == "POST":
            add_user_site(users_sites=user_sites, user_id=user_id)
        else:
            remove_user_site(users_sites=user_sites, user_id=user_id)

        res = jsonify()

        session = update_session(sid, admin_user_id)
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
        
@v1.route("/regions", methods=["POST"])
def createRegion() -> None:
    """
    Create a new region.

    Body:
        name: str,

    Response:
        200: None
        400: str
        500: str
    """
    try:
        if not request.cookies.get(cookie_name):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()
        elif not "name" in request.json or not request.json["name"]:
            logger.error("no name")
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
        
        # check permission
        check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]

        create_region(name=name)

        res = jsonify()

        session = update_session(sid, user_id)
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

@v1.route("/regions/<int:region_id>/sites", methods=["POST"])
def createSite(region_id: int) -> None:
    """
    Create a new site.

    Parameters:
        region_id: int

    Body:
        name: str,

    Response:
        200: None
        400: str
        500: str
    """
    try:
        if not request.cookies.get(cookie_name):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()
        elif not "name" in request.json or not request.json["name"]:
            logger.error("no name")
            raise BadRequest()
        elif not "site_code" in request.json or not request.json["site_code"]:
            logger.error("no site_code")
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
        
        # check permission
        check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]
        site_code = request.json["site_code"]

        create_site(name=name, region_id=region_id, site_code=site_code)

        res = jsonify()

        session = update_session(sid, user_id)
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