import logging
logger = logging.getLogger(__name__)

import json 

# configurations
from Configs import baseConfig
config = baseConfig()
api = config["API"]
cookie_name = api['COOKIE_NAME']

from flask import Blueprint, request, jsonify
v1 = Blueprint("v1", __name__)

from security.cookie import Cookie
from datetime import datetime, timedelta

# database connectors
from schemas.users.baseModel import users_db
from schemas.sites.baseModel import sites_db
from schemas.records.baseModel import records_db

# models
from models.verify_users import verify_user
from models.create_sessions import create_session
from models.update_sessions import update_session
from models.create_users import create_user
from models.change_account_status import update_account_status
from models.find_sessions import find_session
from models.create_records import create_record
from models.find_records import find_record
from models.create_specimen_collections import create_specimen_collection
from models.find_specimen_collections import find_specimen_collection
from models.create_labs import create_lab
from models.find_labs import find_lab
from models.create_follow_ups import create_follow_up
from models.find_follow_ups import find_follow_up
from models.find_outcome_recorded import find_outcome_recorded
from models.create_outcome_recorded import create_outcome_recorded
from models.create_tb_treatment_outcomes import create_tb_treatment_outcome
from models.find_tb_treatment_outcomes import find_tb_treatment_outcome
from models.find_users import find_user
from models.get_regions import get_all_regions
from models.get_sites import get_all_sites

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
def signup():
    """
    Create a new user.

    Body:
        email: str,
        password: str,
        phone_number: str,
        name: str,
        occupation: str,
        site_id: int,
        region_id: int
    
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

        email = request.json["email"]
        password = request.json["password"]
        phone_number = request.json["phone_number"]
        name = request.json["name"]
        site_id = request.json["site_id"]
        occupation = request.json["occupation"]

        user = create_user(
            email, 
            password, 
            phone_number,
            name,
            occupation,
            site_id 
        )
        update_account_status(user, "approved")

        res = jsonify(user)

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

@v1.route("/login", methods=["POST"])
def login():
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

        user = verify_user(email, password)
        session = create_session(user["id"], user_agent)

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

    Parameters:
        region_id: int,
        site_id: int

    Body:
        records_name: str,
        records_age: int,
        records_sex: str,
        records_date_of_test_request: str,
        records_address: str,
        records_telephone: str,
        records_telephone_2: str,
        records_has_art_unique_code: str,
        records_art_unique_code: str,
        records_status: str,
        records_ward_bed_number: str,
        records_currently_pregnant: str,
        records_symptoms_current_cough: str,
        records_symptoms_fever: bool,
        records_symptoms_night_sweats: bool,
        records_symptoms_weight_loss: bool,
        records_symptoms_none_of_the_above: bool,
        records_patient_category_hospitalized: bool,
        records_patient_category_child: bool,
        records_patient_category_to_initiate_art: bool,
        records_patient_category_on_art_symptomatic: bool,
        records_patient_category_outpatient: bool,
        records_patient_category_anc: bool,
        records_patient_category_diabetes_clinic: bool,
        records_patient_category_other: str,
        records_reason_for_test_presumptive_tb: bool,
        records_tb_treatment_history: str,
        records_tb_treatment_history_contact_of_tb_patient: str
    
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

        user_id = find_session(sid, uid, user_agent, user_cookie)

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
            request.json["records_patient_category_other"],
            request.json["records_reason_for_test_presumptive_tb"],
            request.json["records_tb_treatment_history"],
            request.json["records_tb_treatment_history_contact_of_tb_patient"]
        )
       
        create_record(*payload)

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

        user_id = find_session(sid, uid, user_agent, user_cookie)
        
        user = find_user(user_id=user_id)

        result = []

        for site in user["users_sites"]:
            payload = (
                site["id"],
                site["region"]["id"],
                user["id"],
            )
        
            for record in find_record(*payload):
                result.append(record)

        res = jsonify(result)

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

        user_id = find_session(sid, uid, user_agent, user_cookie)

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
       
        create_specimen_collection(*payload)

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

        user_id = find_session(sid, uid, user_agent, user_cookie)
               
        result = find_specimen_collection(specimen_collection_records_id=record_id)

        res = jsonify(result)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
        
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/labs", methods=["POST"])
def createLabRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)

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
            request.json["lab_xpert_mtb_rif_assay_date"],
            request.json["lab_xpert_mtb_rif_assay_done_by"],
            request.json["lab_urine_lf_lam_result"],
            request.json["lab_urine_lf_lam_date"],
            request.json["lab_urine_lf_lam_done_by"],
        )
       
        result = create_lab(*payload)

        return result, 200

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

@v1.route("/users/<int:user_id>/records/<int:record_id>/labs", methods=["GET"])
def findLabRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)
       
        result = find_lab(lab_records_id=record_id)

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500
    
@v1.route("/users/<int:user_id>/records/<int:record_id>/follow_ups", methods=["POST"])
def createFollowUpRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["follow_up_xray"],
            request.json["follow_up_amoxicillin"],
            request.json["follow_up_other_antibiotic"],
            request.json["follow_up_schedule_date"],
            request.json["follow_up_comments"]
        )
       
        result = create_follow_up(*payload)

        return result, 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/follow_ups", methods=["GET"])
def findFollowUpRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)
       
        result = find_follow_up(follow_up_records_id=record_id)

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/outcome_recorded", methods=["POST"])
def createOutcomeRecoredRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["outcome_recorded_started_tb_treatment_outcome"],
            request.json["outcome_recorded_tb_rx_number"],
            request.json["outcome_recorded_other"],
            request.json["outcome_recorded_comments"]
        )
       
        result = create_outcome_recorded(*payload)

        return result, 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/outcome_recorded", methods=["GET"])
def findOutcomeRecoredRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)

        result = find_outcome_recorded(outcome_recorded_records_id=record_id)

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/tb_treatment_outcomes", methods=["POST"])
def createTbTreatmentOutcomeRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)

        payload = (
            record_id,
            user_id,
            request.json["tb_treatment_outcome_result"],
            request.json["tb_treatment_outcome_comments"],
            request.json["tb_treatment_outcome_close_patient_file"]
        )
       
        result = create_tb_treatment_outcome(*payload)

        return result, 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>/records/<int:record_id>/tb_treatment_outcomes", methods=["GET"])
def findTbTreatmentOutcomeRecord(user_id, record_id):
    """
    """
    try:
        find_user(user_id=user_id)
       
        result = find_tb_treatment_outcome(tb_treatment_outcome_records_id=record_id)

        return jsonify(result), 200

    except BadRequest as err:
        return str(err), 400

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<int:user_id>", methods=["GET"])
def findAUser(user_id):
    """
    """
    try:
        user = find_user(user_id=user_id)
       
        return jsonify(user), 200

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

@v1.route("/regions", methods=["GET"])
def getRegions():
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
        result = get_all_regions()

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
def getSites(region_id):
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
        result = get_all_sites(region_id= region_id)

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

