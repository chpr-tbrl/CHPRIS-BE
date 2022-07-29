import logging
logger = logging.getLogger(__name__)

import json 
from threading import Thread

# configurations
from Configs import baseConfig
config = baseConfig()
api = config["API"]
cookie_name = api['COOKIE_NAME']

from flask import Blueprint, after_this_request
from flask import Response
from flask import request
from flask import jsonify

v1 = Blueprint("v1", __name__)

from security.cookie import Cookie

from datetime import timedelta
from datetime import date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

# database connectors
from schemas.users.baseModel import users_db
from schemas.sites.baseModel import sites_db
from schemas.records.baseModel import records_db

# models
from models.users import User_Model
from models.sites import Site_Model
from models.records import Record_Model
from models.sessions import Session_Model
from models.exports import Export_Model
from models.contacts import Contact_Model
from models.sms_notifications import SMS_Model

# exceptions
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

@v1.route("/signup", methods=["POST"])
def signup() -> None:
    """
    Create a new user.

    Body:
        email: str,
        password: str,
        phone_number: str,
        name: str,
        occupation: str,
        site_id: int,
    
    Response:
        200: None,
        400: str,
        401: str,
        409: str,
        500: str
    """
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
        elif not "site_id" in request.json or not request.json["site_id"]:
            logger.error("no site_id")
            raise BadRequest()
        elif not "sms_notifications_type" in request.json or not request.json["sms_notifications_type"]:
            logger.error("no sms_notifications_type")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        phone_number = request.json["phone_number"]
        name = request.json["name"]
        site_id = request.json["site_id"]
        occupation = request.json["occupation"]
        sms_notifications_type = request.json["sms_notifications_type"]

        User = User_Model()

        User.create(
            email=email, 
            password=password, 
            phone_number=phone_number,
            name=name,
            occupation=occupation,
            site_id=site_id,
            sms_notifications_type=sms_notifications_type
        )

        return "", 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/login", methods=["POST"])
def login() -> dict:
    """
    Authenticate a user.

    Body:
        email: str,
        password: str
    
    Response:
        200: dict,
        400: str,
        401: str,
        409: str,
        500: str
    """
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

        User = User_Model()

        user = User.authenticate(email=email, password=password)

        res = jsonify(user)

        Session = Session_Model()

        session = Session.create(unique_identifier=user["id"], user_agent=user_agent)

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

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/regions/<int:region_id>/sites/<int:site_id>/records", methods=["POST"])
def createRecord(region_id: int, site_id: int) -> None:
    """
    Create a new record.
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

        User.check_account_status(user_id=user_id)

        payload = (
            site_id,
            region_id,
            user_id,
            request.json["records_name"],
            request.json["records_age"],
            request.json["records_sex"],
            request.json["records_date_of_test_request"],
            request.json["records_address"],
            request.json["records_telephone"],
            request.json["records_telephone_2"],
            request.json["records_has_art_unique_code"],
            request.json["records_art_unique_code"],
            request.json["records_status"],
            request.json["records_ward_bed_number"],
            request.json["records_currently_pregnant"],
            request.json["records_symptoms_current_cough"],
            request.json["records_symptoms_fever"],
            request.json["records_symptoms_night_sweats"],
            request.json["records_symptoms_weight_loss"],
            request.json["records_symptoms_none_of_the_above"],
            request.json["records_patient_category_hospitalized"],
            request.json["records_patient_category_child"],
            request.json["records_patient_category_to_initiate_art"],
            request.json["records_patient_category_on_art_symptomatic"],
            request.json["records_patient_category_outpatient"],
            request.json["records_patient_category_anc"],
            request.json["records_patient_category_diabetes_clinic"],
            request.json["records_patient_category_prisoner"],
            request.json["records_patient_category_other"],
            request.json["records_reason_for_test"],
            request.json["records_reason_for_test_follow_up_months"],
            request.json["records_tb_treatment_history"],
            request.json["records_tb_treatment_history_contact_of_tb_patient"],
            request.json["records_tb_treatment_history_other"],
            request.json["records_tb_type"],
            request.json["records_tb_treatment_number"],
            request.json["records_sms_notifications"],
            request.json["records_requester_name"],
            request.json["records_requester_telephone"]
        )
       
        Record = Record_Model()

        Record.create_record(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/regions/<int:region_id>/sites/<int:site_id>/records/<int:record_id>", methods=["PUT"])
def updateRecord(region_id: int, site_id: int, record_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            site_id,
            region_id,
            record_id,
            request.json["records_name"],
            request.json["records_age"],
            request.json["records_sex"],
            request.json["records_date_of_test_request"],
            request.json["records_address"],
            request.json["records_telephone"],
            request.json["records_telephone_2"],
            request.json["records_has_art_unique_code"],
            request.json["records_art_unique_code"],
            request.json["records_status"],
            request.json["records_ward_bed_number"],
            request.json["records_currently_pregnant"],
            request.json["records_symptoms_current_cough"],
            request.json["records_symptoms_fever"],
            request.json["records_symptoms_night_sweats"],
            request.json["records_symptoms_weight_loss"],
            request.json["records_symptoms_none_of_the_above"],
            request.json["records_patient_category_hospitalized"],
            request.json["records_patient_category_child"],
            request.json["records_patient_category_to_initiate_art"],
            request.json["records_patient_category_on_art_symptomatic"],
            request.json["records_patient_category_outpatient"],
            request.json["records_patient_category_anc"],
            request.json["records_patient_category_diabetes_clinic"],
            request.json["records_patient_category_prisoner"],
            request.json["records_patient_category_other"],
            request.json["records_reason_for_test"],
            request.json["records_reason_for_test_follow_up_months"],
            request.json["records_tb_treatment_history"],
            request.json["records_tb_treatment_history_contact_of_tb_patient"],
            request.json["records_tb_treatment_history_other"],
            request.json["records_tb_type"],
            request.json["records_tb_treatment_number"],
            request.json["records_sms_notifications"],
            request.json["records_requester_name"],
            request.json["records_requester_telephone"]
        )
       
        Record = Record_Model()

        Record.update_record(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records", methods=["GET"])
def findRecord() -> list:
    """
    Find records that belong to user's site.

    Parameters:
        None

    Body:
       None
    
    Response:
        200: list,
        400: str,
        401: str,
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

        user = User.fetch_user(user_id=user_id, account_status="approved")

        records_name = request.args.get("name") or None
        records_id = request.args.get("id") or None
        records_telephone = request.args.get("telephone") or None
        records_site_id = request.args.get("site_id") or None
        records_region_id = request.args.get("region_id") or None


        result = []

        Record = Record_Model()

        if records_id:
            if not records_site_id:
                logger.error("no site_id")
                raise BadRequest()
            elif not records_region_id:
                logger.error("no region_id")
                raise BadRequest()

            payload = (
                records_site_id,
                records_region_id,
                user["id"],
                user["permitted_decrypted_data"],
                records_name,
                records_id,
                records_telephone
            )

            for record in Record.fetch_records(*payload):
                result.append(record)
        else:
            for site in user["users_sites"]:
                payload = (
                    site["id"],
                    site["region"]["id"],
                    user["id"],
                    user["permitted_decrypted_data"],
                    records_name,
                    records_id,
                    records_telephone
                )

                for record in Record.fetch_records(*payload):
                    result.append(record)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>", methods=["GET"])
def findSingleRecord(record_id: int) -> list:
    """
    Find single record that belong to user's site.

    Parameters:
        record_id: int

    Body:
       None
    
    Response:
        200: list,
        400: str,
        401: str,
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

        user = User.fetch_user(user_id=user_id, account_status="approved")

        result = []

        for site in user["users_sites"]:
            payload = (
                record_id,
                site["id"],
                site["region"]["id"],
                user["id"],
                user["permitted_decrypted_data"]
            )

            Record = Record_Model()

            for record in Record.fetch_record(*payload):
                result.append(record)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/specimen_collections", methods=["POST"])
def createSpecimenCollectionRecord(record_id: int) -> None:
    """
    Create a new specimen_collections record.

    Parameters:
        record_id: int

    Body:
        specimen_collection_1_date: str,
        specimen_collection_1_specimen_collection_type: str,
        specimen_collection_1_other: str,
        specimen_collection_1_period: str,
        specimen_collection_1_aspect: str,
        specimen_collection_1_received_by: str,
        specimen_collection_2_date: str,
        specimen_collection_2_specimen_collection_type: str,
        specimen_collection_2_other: str,
        specimen_collection_2_period: str,
        specimen_collection_2_aspect: str,
        specimen_collection_2_received_by: str
            
    Response:
        200: None,
        400: str,
        401: str,
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

        User.check_account_status(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["specimen_collection_1_date"],
            request.json["specimen_collection_1_specimen_collection_type"],
            request.json["specimen_collection_1_other"],
            request.json["specimen_collection_1_period"],
            request.json["specimen_collection_1_aspect"],
            request.json["specimen_collection_1_received_by"],
            request.json["specimen_collection_2_date"],
            request.json["specimen_collection_2_specimen_collection_type"],
            request.json["specimen_collection_2_other"],
            request.json["specimen_collection_2_period"],
            request.json["specimen_collection_2_aspect"],
            request.json["specimen_collection_2_received_by"],
        )

        Record = Record_Model()
       
        Record.create_specimen_collection(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/specimen_collections/<int:specimen_collection_id>", methods=["PUT"])
def updateSpecimenCollectionRecord(specimen_collection_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            specimen_collection_id,
            request.json["specimen_collection_1_date"],
            request.json["specimen_collection_1_specimen_collection_type"],
            request.json["specimen_collection_1_other"],
            request.json["specimen_collection_1_period"],
            request.json["specimen_collection_1_aspect"],
            request.json["specimen_collection_1_received_by"],
            request.json["specimen_collection_2_date"],
            request.json["specimen_collection_2_specimen_collection_type"],
            request.json["specimen_collection_2_other"],
            request.json["specimen_collection_2_period"],
            request.json["specimen_collection_2_aspect"],
            request.json["specimen_collection_2_received_by"],
        )

        Record = Record_Model()
       
        Record.update_specimen_collection(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/specimen_collections", methods=["GET"])
def findSpecimenCollectionRecord(record_id: int) -> list:
    """
    Find specimen_collection records that belong to record_id.

    Parameters:
        record_id: int

    Body:
       None
    
    Response:
        200: list,
        400: str,
        401: str,
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

        User.check_account_status(user_id=user_id)
               
        Record = Record_Model()

        result = Record.fetch_specimen_collection(specimen_collection_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/labs", methods=["POST"])
def createLabRecord(record_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            record_id,            
            user_id,
            request.json["lab_date_specimen_collection_received"],
            request.json["lab_received_by"],
            request.json["lab_registration_number"],
            request.json["lab_smear_microscopy_result_result_1"],
            request.json["lab_smear_microscopy_result_result_2"],
            request.json["lab_smear_microscopy_result_date"],
            request.json["lab_smear_microscopy_result_done_by"],
            request.json["lab_xpert_mtb_rif_assay_result"],
            request.json["lab_xpert_mtb_rif_assay_grades"],
            request.json["lab_xpert_mtb_rif_assay_rif_result"],
            request.json["lab_xpert_mtb_rif_assay_result_2"],
            request.json["lab_xpert_mtb_rif_assay_grades_2"],
            request.json["lab_xpert_mtb_rif_assay_rif_result_2"],
            request.json["lab_xpert_mtb_rif_assay_date"],
            request.json["lab_xpert_mtb_rif_assay_done_by"],
            request.json["lab_urine_lf_lam_result"],
            request.json["lab_urine_lf_lam_date"],
            request.json["lab_urine_lf_lam_done_by"],
            request.json["lab_culture_mgit_culture"],
            request.json["lab_culture_lj_culture"],
            request.json["lab_culture_date"],
            request.json["lab_culture_done_by"],
            request.json["lab_lpa_mtbdrplus_isoniazid"],
            request.json["lab_lpa_mtbdrplus_rifampin"],
            request.json["lab_lpa_mtbdrs_flouoroquinolones"],
            request.json["lab_lpa_mtbdrs_kanamycin"],
            request.json["lab_lpa_mtbdrs_amikacin"],
            request.json["lab_lpa_mtbdrs_capreomycin"],
            request.json["lab_lpa_mtbdrs_low_level_kanamycin"],
            request.json["lab_lpa_date"],
            request.json["lab_lpa_done_by"],
            request.json["lab_dst_isonazid"],
            request.json["lab_dst_rifampin"],
            request.json["lab_dst_ethambutol"],
            request.json["lab_dst_kanamycin"],
            request.json["lab_dst_ofloxacin"],
            request.json["lab_dst_levofloxacinekanamycin"],
            request.json["lab_dst_moxifloxacinekanamycin"],
            request.json["lab_dst_amikacinekanamycin"],
            request.json["lab_dst_date"],
            request.json["lab_dst_done_by"]
        )
       
        Record = Record_Model()

        lab_id = Record.create_lab(*payload)

        Contact = Contact_Model()
        
        Sms = SMS_Model()

        def trigger_sms(record_id: int, lab_id: int, contacts: dict) -> None:
            """
            """
            Sms.send_lab(record_id=record_id, lab_id=lab_id, contacts=contacts['lab'])
            Sms.send_requester(record_id=record_id, lab_id=lab_id, contacts=contacts['requester'])
            Sms.send_client(contacts=contacts['client'])

            return None

        logger.debug("lab_result_type: %s" % request.json["lab_result_type"])
        if request.json["lab_result_type"] == "positive":
            contacts = Contact.all(record_id=record_id, sms_notification_type="positive,all")

            @after_this_request
            def send_sms(response):
                thread = Thread(target=trigger_sms, kwargs={'record_id': record_id, 'lab_id': int(lab_id), 'contacts': contacts})
                thread.start()
                return response

        elif request.json["lab_result_type"] == "negative":
            contacts = Contact.all(record_id=record_id, sms_notification_type="all")

            @after_this_request
            def send_sms(response):
                thread = Thread(target=trigger_sms, kwargs={'record_id': record_id, 'lab_id': int(lab_id), 'contacts': contacts})
                thread.start()
                return response
        else:
            pass

        res = Response()

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/labs/<int:lab_id>", methods=["PUT"])
def updateLabRecord(lab_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            lab_id,
            request.json["lab_date_specimen_collection_received"],
            request.json["lab_received_by"],
            request.json["lab_registration_number"],
            request.json["lab_smear_microscopy_result_result_1"],
            request.json["lab_smear_microscopy_result_result_2"],
            request.json["lab_smear_microscopy_result_date"],
            request.json["lab_smear_microscopy_result_done_by"],
            request.json["lab_xpert_mtb_rif_assay_result"],
            request.json["lab_xpert_mtb_rif_assay_grades"],
            request.json["lab_xpert_mtb_rif_assay_rif_result"],
            request.json["lab_xpert_mtb_rif_assay_result_2"],
            request.json["lab_xpert_mtb_rif_assay_grades_2"],
            request.json["lab_xpert_mtb_rif_assay_rif_result_2"],
            request.json["lab_xpert_mtb_rif_assay_date"],
            request.json["lab_xpert_mtb_rif_assay_done_by"],
            request.json["lab_urine_lf_lam_result"],
            request.json["lab_urine_lf_lam_date"],
            request.json["lab_urine_lf_lam_done_by"],
            request.json["lab_culture_mgit_culture"],
            request.json["lab_culture_lj_culture"],
            request.json["lab_culture_date"],
            request.json["lab_culture_done_by"],
            request.json["lab_lpa_mtbdrplus_isoniazid"],
            request.json["lab_lpa_mtbdrplus_rifampin"],
            request.json["lab_lpa_mtbdrs_flouoroquinolones"],
            request.json["lab_lpa_mtbdrs_kanamycin"],
            request.json["lab_lpa_mtbdrs_amikacin"],
            request.json["lab_lpa_mtbdrs_capreomycin"],
            request.json["lab_lpa_mtbdrs_low_level_kanamycin"],
            request.json["lab_lpa_date"],
            request.json["lab_lpa_done_by"],
            request.json["lab_dst_isonazid"],
            request.json["lab_dst_rifampin"],
            request.json["lab_dst_ethambutol"],
            request.json["lab_dst_kanamycin"],
            request.json["lab_dst_ofloxacin"],
            request.json["lab_dst_levofloxacinekanamycin"],
            request.json["lab_dst_moxifloxacinekanamycin"],
            request.json["lab_dst_amikacinekanamycin"],
            request.json["lab_dst_date"],
            request.json["lab_dst_done_by"]
        )
       
        Record = Record_Model()

        record_id = Record.update_lab(*payload)

        Contact = Contact_Model()
        
        Sms = SMS_Model()

        def trigger_sms(record_id: int, lab_id: int, contacts: dict) -> None:
            """
            """
            Sms.send_lab(record_id=record_id, lab_id=lab_id, contacts=contacts['lab'])
            Sms.send_requester(record_id=record_id, lab_id=lab_id, contacts=contacts['requester'])
            Sms.send_client(contacts=contacts['client'])

            return None

        logger.debug("lab_result_type: %s" % request.json["lab_result_type"])
        if request.json["lab_result_type"] == "positive":
            contacts = Contact.all(record_id=record_id, sms_notification_type="positive,all")

            @after_this_request
            def send_sms(response):
                thread = Thread(target=trigger_sms, kwargs={'record_id': record_id, 'lab_id': lab_id, 'contacts': contacts})
                thread.start()
                return response

        elif request.json["lab_result_type"] == "negative":
            contacts = Contact.all(record_id=record_id, sms_notification_type="all")

            @after_this_request
            def send_sms(response):
                thread = Thread(target=trigger_sms, kwargs={'record_id': record_id, 'lab_id': lab_id, 'contacts': contacts})
                thread.start()
                return response
        else:
            pass

        res = Response()
        
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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/labs", methods=["GET"])
def findLabRecord(record_id: int) -> list:
    """
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

        User.check_account_status(user_id=user_id)
       
        Record = Record_Model()

        result = Record.fetch_lab(lab_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500
    
@v1.route("/records/<int:record_id>/follow_ups", methods=["POST"])
def createFollowUpRecord(record_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["follow_up_xray"],
            request.json["follow_up_amoxicillin"],
            request.json["follow_up_other_antibiotic"],
            request.json["follow_up_schedule_date"],
            request.json["follow_up_comments"]
        )

        Record = Record_Model()

        Record.create_follow_up(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/follow_ups/<int:follow_up_id>", methods=["PUT"])
def updateFollowUpRecord(follow_up_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            follow_up_id,
            request.json["follow_up_xray"],
            request.json["follow_up_amoxicillin"],
            request.json["follow_up_other_antibiotic"],
            request.json["follow_up_schedule_date"],
            request.json["follow_up_comments"]
        )

        Record = Record_Model()

        Record.update_follow_up(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/follow_ups", methods=["GET"])
def findFollowUpRecord(record_id: int) -> list:
    """
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

        User.check_account_status(user_id=user_id)
    
        Record = Record_Model()

        result = Record.fetch_follow_up(follow_up_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/outcome_recorded", methods=["POST"])
def createOutcomeRecoredRecord(record_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["outcome_recorded_started_tb_treatment_outcome"],
            request.json["outcome_recorded_tb_rx_number"],
            request.json["outcome_recorded_other"],
            request.json["outcome_recorded_comments"]
        )
       
        Record = Record_Model()

        Record.create_outcome_recorded(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/outcome_recorded/<int:outcome_recorded_id>", methods=["PUT"])
def updateOutcomeRecoredRecord(outcome_recorded_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)

        payload = (
            outcome_recorded_id,
            request.json["outcome_recorded_started_tb_treatment_outcome"],
            request.json["outcome_recorded_tb_rx_number"],
            request.json["outcome_recorded_other"],
            request.json["outcome_recorded_comments"]
        )
       
        Record = Record_Model()

        Record.update_outcome_recorded(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/outcome_recorded", methods=["GET"])
def findOutcomeRecoredRecord(record_id: int) -> list:
    """
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

        User.check_account_status(user_id=user_id)

        Record = Record_Model()

        result = Record.fetch_outcome_recorded(outcome_recorded_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/tb_treatment_outcomes", methods=["POST"])
def createTbTreatmentOutcomeRecord(record_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)
        
        payload = (
            record_id,
            user_id,
            request.json["tb_treatment_outcome_result"],
            request.json["tb_treatment_outcome_comments"],
            request.json["tb_treatment_outcome_close_patient_file"]
        )
       
        Record = Record_Model()

        Record.create_tb_treatment_outcome(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/tb_treatment_outcomes/<int:tb_treatment_outcomes_id>", methods=["PUT"])
def updateTbTreatmentOutcomeRecord(tb_treatment_outcomes_id: int) -> None:
    """
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

        User.check_account_status(user_id=user_id)
        
        payload = (
            tb_treatment_outcomes_id,
            request.json["tb_treatment_outcome_result"],
            request.json["tb_treatment_outcome_comments"],
            request.json["tb_treatment_outcome_close_patient_file"]
        )
       
        Record = Record_Model()

        Record.update_tb_treatment_outcome(*payload)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/records/<int:record_id>/tb_treatment_outcomes", methods=["GET"])
def findTbTreatmentOutcomeRecord(record_id: int) -> list:
    """
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

        User.check_account_status(user_id=user_id)

        Record = Record_Model()

        result = Record.fetch_tb_treatment_outcome(tb_treatment_outcome_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/profile", methods=["GET"])
def findAUser() -> dict:
    """
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

        user = User.fetch_user(user_id=user_id, account_status="approved")
       
        res = jsonify(user)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users", methods=["PUT", "POST"])
def updateProfile() -> None:
    """
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

        User.check_account_status(user_id=user_id)

        if request.method == "PUT":
            if not "phone_number" in request.json or not request.json["phone_number"]:
                logger.error("no phone_number")
                raise BadRequest()
            elif not "name" in request.json or not request.json["name"]:
                logger.error("no name")
                raise BadRequest()
            elif not "occupation" in request.json or not request.json["occupation"]:
                logger.error("no occupation")
                raise BadRequest()
            elif not "sms_notifications" in request.json or not request.json["sms_notifications"]:
                logger.error("no sms_notifications")
                raise BadRequest()
            elif not "sms_notifications_type" in request.json or not request.json["sms_notifications_type"]:
                logger.error("no sms_notifications_type")
                raise BadRequest()

            phone_number = request.json["phone_number"]
            name = request.json["name"]
            occupation = request.json["occupation"]
            sms_notifications = request.json["sms_notifications"]
            sms_notifications_type = request.json["sms_notifications_type"]

            User.update_profile(
                id=user_id,
                phone_number=phone_number,
                name=name,
                occupation=occupation,
                sms_notifications=sms_notifications,
                sms_notifications_type=sms_notifications_type
            )

        elif request.method == "POST":
            if not "current_password" in request.json or not request.json["current_password"]:
                logger.error("no current_password")
                raise BadRequest()
            elif not "new_password" in request.json or not request.json["new_password"]:
                logger.error("no new_password")
                raise BadRequest()

            current_password = request.json["current_password"]
            new_password = request.json["new_password"]

            User.update_password(
                id=user_id,
                current_password=current_password,
                new_password=new_password
            )
       
        res = Response()

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/regions", methods=["GET"])
def getRegions() -> list:
    """
    Get all regions.

    Body:
        None

    Response:
        200: list,
        400: str,       
        401: str,
        500: str
    """
    try:       
        Site = Site_Model()

        result = Site.fetch_regions()

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/regions/<int:region_id>/sites", methods=["GET"])
def getSites(region_id) -> list:
    """
    Get all sites for a region.

    Parameters:
        region_id: int

    Body:
        None

    Response:
        200: list,
        400: str,       
        401: str,
        500: str
    """
    try:        
        Site = Site_Model()

        result = Site.fetch_sites(region_id= region_id)

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/regions/<string:region_id>/sites/<string:site_id>/exports/<string:format>", methods=["GET"])
def dataExport(region_id: str, site_id: str, format: str) -> str:
    """
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
        
        user = User.fetch_user(user_id=user_id, no_sites=True, account_status="approved")

        if user['permitted_export_range'] < 1:
            logger.error("Not allowed to export. permitted_export_range < 1")
            raise Forbidden()
        elif len(user['permitted_export_types']) < 1:
            logger.error("Not allowed to export. No permitted_export_types")
            raise Forbidden()
        elif not format in user['permitted_export_types']:
            logger.error("Not allowed to export %s" % format)
            raise Forbidden()

        permitted_decrypted_data= user["permitted_decrypted_data"]

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        month_range = date.today().month - parse(start_date).month

        logger.debug("checking permitted_export_range ...")
        if (month_range+1) > user['permitted_export_range']:
            logger.error("Not allowed to export. Permitted_export_range exceeded")
            raise Forbidden()

        start_date = parse(start_date)
        end_date = parse(end_date) + relativedelta(hours=23, minutes=59, seconds=59)
        req_range = end_date.month - start_date.month
                
        logger.info("requesting %d month(s) data" % (req_range+1))

        Export = Export_Model()
        
        if format == "csv":
            download_path = Export.csv(start_date=start_date, end_date=end_date, region_id=region_id, site_id=site_id, permitted_decrypted_data=permitted_decrypted_data)

            res = Response(download_path)
        elif format == "pdf":
            pdf_data = Export.pdf(start_date=start_date, end_date=end_date, region_id=region_id, site_id=site_id, permitted_decrypted_data=permitted_decrypted_data)

            res = jsonify(pdf_data)

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

@v1.route("/logout", methods=["POST"])
def logout() -> None:
    """
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

        Session.find(sid=sid, unique_identifier=uid, user_agent=user_agent, cookie=user_cookie) 

        res = Response()

        res.delete_cookie(cookie_name)

        logger.info("- Successfully cleared cookie")

        return res, 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Forbidden as err:
        return str(err), 403

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500