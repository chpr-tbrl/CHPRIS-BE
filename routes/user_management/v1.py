import logging
import json
import werkzeug

logger = logging.getLogger(__name__)

from Configs import configuration
from error import BadRequest, Forbidden, InternalServerError, Unauthorized, Conflict
from flask import Blueprint, request, jsonify
from security import Cookie
from datetime import timedelta
from schemas.users.baseModel import users_db
from schemas.sites.baseModel import sites_db
from schemas.records.baseModel import records_db

v1 = Blueprint("v1", __name__)
config = configuration()
api = config["API"]
cookie_name = api['COOKIE_NAME']

from models.verify_users import verify_user
from models.create_sessions import create_session
from models.update_sessions import update_session
from models.create_users import create_user
from models.change_states import change_state
from models.find_sessions import find_session
from models.get_users import get_all_users
from models.create_records import create_record
from models.get_records import get_all_records
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
from models.assign_user_roles import assign_role

@v1.after_request
def after_request(response):
    users_db.close()
    sites_db.close()
    records_db.close()
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
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
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
        # elif not request.headers.get("User-Agent"):
        #     logger.error("no user agent")
        #     raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        # user_agent = request.headers.get("User-Agent")

        user = verify_user(email, password)
        # session = create_session(user["uid"], user_agent)

        res = jsonify(user)

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
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
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

@v1.route("/users", methods=["GET"])
def getAllUsers():
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
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
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

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records", methods=["POST"])
def createRecord(user_id, site_id, region_id):
    try:

        userId = user_id
        siteId = site_id
        regionId = region_id

        payload = (
            siteId,
            regionId,
            userId,
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
       
        result = create_record(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records", methods=["GET"])
def findRecord(user_id, site_id, region_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id

        payload = (
            siteId,
            regionId,
            userId
        )
       
        result = find_record(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/specimen_collections", methods=["POST"])
def createSpecimenCollectionRecord(user_id, site_id, region_id, record_id):
    try:

        userId = user_id
        siteId = site_id
        regionId = region_id
        specimen_collection_records_id = record_id

        payload = (
            specimen_collection_records_id,
            userId,
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
       
        result = create_specimen_collection(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/specimen_collections", methods=["GET"])
def findSpecimenCollectionRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        specimen_collection_records_id = record_id

        payload = (
            userId,
            specimen_collection_records_id
        )
       
        result = find_specimen_collection(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/labs", methods=["POST"])
def createLabRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        lab_records_id = record_id

        payload = (
            lab_records_id,            
            userId,
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

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/labs", methods=["GET"])
def findLabRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        lab_records_id = record_id

        payload = (
            userId,
            lab_records_id
        )
       
        result = find_lab(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500
    
@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/follow_ups", methods=["POST"])
def createFollowUpRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        follow_up_records_id = record_id

        payload = (
            follow_up_records_id,
            userId,
            request.json["follow_up_xray"],
            request.json["follow_up_amoxicillin"],
            request.json["follow_up_other_antibiotic"],
            request.json["follow_up_schedule_date"],
            request.json["follow_up_comments"]
        )
       
        result = create_follow_up(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/follow_ups", methods=["GET"])
def findFollowUpRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        follow_up_records_id = record_id

        payload = (
            userId,
            follow_up_records_id
        )
       
        result = find_follow_up(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/outcome_recorded", methods=["POST"])
def createOutcomeRecoredRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        outcome_recorded_records_id = record_id

        payload = (
            outcome_recorded_records_id,
            userId,
            request.json["outcome_recorded_started_tb_treatment_outcome"],
            request.json["outcome_recorded_tb_rx_number"],
            request.json["outcome_recorded_other"],
            request.json["outcome_recorded_comments"]
        )
       
        result = create_outcome_recorded(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/outcome_recorded", methods=["GET"])
def findOutcomeRecoredRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        outcome_recorded_records_id = record_id

        payload = (
            userId,
            outcome_recorded_records_id
        )
       
        result = find_outcome_recorded(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/tb_treatment_outcomes", methods=["POST"])
def createTbTreatmentOutcomeRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        tb_treatment_outcome_records_id = record_id

        payload = (
            tb_treatment_outcome_records_id,
            userId,
            request.json["tb_treatment_outcome_result"],
            request.json["tb_treatment_outcome_comments"],
            request.json["tb_treatment_outcome_close_patient_file"]
        )
       
        result = create_tb_treatment_outcome(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/sites/<site_id>/regions/<region_id>/records/<record_id>/tb_treatment_outcomes", methods=["GET"])
def findTbTreatmentOutcomeRecord(user_id, site_id, region_id, record_id):
    try:
        userId = user_id
        siteId = site_id
        regionId = region_id
        tb_treatment_outcome_records_id = record_id

        payload = (
            userId,
            tb_treatment_outcome_records_id
        )
       
        result = find_tb_treatment_outcome(*payload)

        return jsonify(result), 200
    except (BadRequest, werkzeug.exceptions.BadRequest) as err:
        return str(err), 400
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<user_id>/roles/<role>", methods=["POST"])
def assign_user_role(user_id, role):
    try:
        userId = user_id

        payload = (
            userId,
            role
        )
       
        assign_role(*payload)

        return "", 200
    except BadRequest as err:
        return "%s" % err, 400
    except Unauthorized as err:
        return "%s" % err, 401
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500
    except Exception as err:
        logger.exception(err)
        return "internal server error", 500
