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

from models.users import User_Model
from models.sites import Site_Model
from models.sessions import Session_Model

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

        Session = Session_Model()

        user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=user_id, scope=["admin", "super_admin"])
    
        account_status = request.args.get("account_status")

        users_list = User.fetch_users(account_status=account_status)

        res = jsonify(users_list)

        session = Session.update(sid=sid, unique_identifier=user_id)

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

@v1.route("/users/<int:user_id>", methods=["GET", "POST","PUT"])
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
        # Fetch account
        if request.method == "GET":
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
            
            Session = Session_Model()

            admin_user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 

            User = User_Model()

            user = User.fetch_user(user_id=user_id)

            res = jsonify(user)

            session = Session.update(sid=sid, unique_identifier=admin_user_id)

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
           
        # update account
        elif request.method == "PUT":
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
            
            Session = Session_Model()

            admin_user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
            
            User = User_Model()

            account_type = User.check_permission(user_id=admin_user_id, scope=["admin", "super_admin"])
            
            user = User.fetch_user(user_id=user_id, no_sites=True)

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

            User = User_Model()

            User.update(*payload)

            res = jsonify()

            session = Session.update(sid=sid, unique_identifier=admin_user_id)

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
            
            Session = Session_Model()

            admin_user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
            
            User = User_Model()

            User.check_permission(user_id=admin_user_id, scope=["admin", "super_admin"], permitted_approve_accounts=True)

            account_status = request.json["account_status"]

            User.update_account_status(user_id=user_id, account_status=account_status)

            res = jsonify()

            session = Session.update(sid=sid, unique_identifier=admin_user_id)

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

        Session = Session_Model()

        admin_user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=admin_user_id, scope=["admin", "super_admin"])

        user_sites = request.json

        if request.method == "POST":
            User.add_site(users_sites=user_sites, user_id=user_id)
        else:
            User.remove_site(users_sites=user_sites, user_id=user_id)

        res = jsonify()

        session = Session.update(sid=sid, unique_identifier=admin_user_id)

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

        Session = Session_Model()

        user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]

        Site = Site_Model()

        Site.create_region(name=name)

        res = jsonify()

        session = Session.update(sid=sid, unique_identifier=user_id)

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

@v1.route("/regions/<int:region_id>", methods=["PUT"])
def updateRegion(region_id) -> None:
    """
    Update region.

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

        cookie = Cookie()
        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = json_cookie["uid"]
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        Session = Session_Model()

        user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]

        Site = Site_Model()

        Site.update_region(region_id=region_id, name=name)

        res = jsonify()

        session = Session.update(sid=sid, unique_identifier=user_id)

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
        site_code: str

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

        Session = Session_Model()

        user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]
        site_code = request.json["site_code"]

        Site = Site_Model()

        Site.create_site(name=name, region_id=region_id, site_code=site_code)

        res = jsonify()

        session = Session.update(sid=sid, unique_identifier=user_id)

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

@v1.route("/sites/<int:site_id>", methods=["PUT"])
def updateSite(site_id: int) -> None:
    """
    Update site.

    Parameters:
        site_id: int

    Body:
        name: str,
        site_code: str

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

        Session = Session_Model()

        user_id = Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 
        
        User = User_Model()

        User.check_permission(user_id=user_id, scope=["admin", "super_admin"])

        name = request.json["name"]
        site_code = request.json["site_code"]

        Site = Site_Model()

        Site.update_site(name=name, site_id=site_id, site_code=site_code)

        res = jsonify()

        session = Session.update(sid=sid, unique_identifier=user_id)

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