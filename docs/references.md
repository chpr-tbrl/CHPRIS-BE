# CHPR-IS API References

Manage Users, Sites and Records endpoints

## Endpoints

- [Users](#users)
  1. [Signup](#1-signup)
  1. [Login](#2-login)
  1. [Admin login](#3-admin-login)
  1. [Admin logout](#4-admin-logout)
  1. [Logout](#5-logout)
  1. [Fetch profile](#6-fetch-profile)
  1. [Fetch admin profile](#7-fetch-admin-profile)
  1. [Update profile](#8-update-profile)
  1. [Update admins profile](#9-update-admins-profile)
  1. [Fetch all users](#10-fetch-all-users)
  1. [Fetch a user](#11-fetch-a-user)
  1. [Update a user](#12-update-a-user)
  1. [Update account status](#13-update-account-status)
  1. [Update password](#14-update-password)
  1. [Update admin password](#15-update-admin-password)
  1. [Add sites](#16-add-sites)
  1. [Remove sites](#17-remove-sites)
- [Sites](#sites)
  1. [Create site](#1-create-site)
  1. [Update site](#2-update-site)
  1. [Fetch all sites](#3-fetch-all-sites)
  1. [Create region](#4-create-region)
  1. [Update region](#5-update-region)
  1. [Fetch all regions](#6-fetch-all-regions)
- [Records](#records)
  1. [Create record](#1-create-record)
  1. [Update record](#2-update-record)
  1. [Fetch records](#3-fetch-records)
  1. [Fetch a record](#4-fetch-a-record)
  1. [Create specimen collection](#5-create-specimen-collection)
  1. [Update specimen collection](#6-update-specimen-collection)
  1. [Fetch specimen collections](#7-fetch-specimen-collections)
  1. [Create lab](#8-create-lab)
  1. [Update lab](#9-update-lab)
  1. [Fetch labs](#10-fetch-labs)
  1. [Create follow up](#11-create-follow-up)
  1. [Update follow up](#12-update-follow-up)
  1. [Fetch follow ups](#13-fetch-follow-ups)
  1. [Create outcome recorded](#14-create-outcome-recorded)
  1. [Update outcome recorded](#15-update-outcome-recorded)
  1. [Fetch outcome recorded](#16-fetch-outcome-recorded)
  1. [Create tb treatment outcome](#17-create-tb-treatment-outcome)
  1. [Update tb treatment outcome](#18-update-tb-treatment-outcome)
  1. [Fetch tb treatment outcomes](#19-fetch-tb-treatment-outcomes)
- [Exports](#exports)
  1. [Export data](#1-export-data)

---

## Users

Users endpoints

### 1. Signup

Create a new user's account.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `409` - Conflict
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/signup
```

**_Body:_**

```js
{
    "phone_number":"string",
    "name": "string",
    "email": "string",
    "password": "string",
    "occupation": "string",
    "site_id": "integer",
    "sms_notifications_type": "string"
}
```

### 2. Login

Login to user's account.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/login
```

**_Body:_**

```js
{
    "email": "string",
    "password": "string"
}
```

### 3. Admin login

Login to admin account.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/login
```

**_Body:_**

```js
{
    "email": "string",
    "password": "string"
}
```

### 4. Admin logout

Logout of admin account.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/logout
```

### 5. Logout

Logout of current account.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/logout
```

### 6. Fetch profile

Fetch currently authenticated user's account information.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/profile
```

### 7. Fetch admin profile

Fetch currently authenticated admin user's account information. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/admin/profile
```

### 8. Update profile

Update currently authenticated user's account information.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/users
```

**_Body:_**

```js
{
    "phone_number":"string",
    "name": "string",
    "occupation": "string",
    "sms_notifications": "boolean",
    "sms_notifications_type": "string"
}
```

### 9. Update admins profile

Update currently authenticated admin user's account information. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/admin/users
```

**_Body:_**

```js
{
    "phone_number":"string",
    "name": "string",
    "occupation": "string",
    "sms_notifications": "boolean",
    "sms_notifications_type": "string"
}
```

### 10. Fetch all users

Fetch all users' account information. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/admin/users
```

### 11. Fetch a user

Fetch a user's account information. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/admin/users/{{user_id}}
```

### 12. Update a user

Update a user's account information. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/admin/users/{{user_id}}
```

**_Body:_**

```js
{
    "account_status":"string",
    "permitted_export_types": "array",
    "account_type": "string",
    "permitted_export_range": "integer",
    "permitted_approve_accounts": "boolean",
    "permitted_decrypted_data": "boolean"
}
```

### 13. Update account status

Update a user's account status. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/users/{{user_id}}
```

**_Body:_**

```js
{
    "account_status":"string"
}
```

### 14. Update password

Update a user's password.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/users
```

**_Body:_**

```js
{
    "current_password":"string",
    "new_password":"string"
}
```

### 15. Update admin password

Update admin user's password. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/users
```

**_Body:_**

```js
{
    "current_password":"string",
    "new_password":"string"
}
```

### 16. Add sites

Add a list of sites to a user's account. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/users/{{user_id}}/sites
```

**_Body:_**

```js
[];
```

### 17. Remove sites

Remove a list of sites to a user's account. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: DELETE
Content-Type: application/json
URL: {{domain}}/v1/admin/users/{{user_id}}/sites
```

**_Body:_**

```js
[];
```

## Sites

Sites endpoints

### 1. Create site

Add a new site to the database. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/regions/{{region_id}}/sites
```

**_Body:_**

```js
{
    "name": "string",
    "site_code": "string"
}
```

### 2. Update site

Update a site. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/admin/sites/{{site_id}}
```

**_Body:_**

```js
{
    "name": "string",
    "site_code": "string"
}
```

### 3. Fetch all sites

Fetch all sites.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/regions/{{region_id}}/sites
```

### 4. Create region

Add a new region to the database. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/admin/regions
```

**_Body:_**

```js
{
    "name": "string",
    "region_code": "string"
}
```

### 5. Update region

Update a region. Only permitted accounts can perform this action.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/admin/regions/{{region_id}}
```

**_Body:_**

```js
{
    "name": "string",
    "region_code":"string"
}
```

### 6. Fetch all regions

Fetch all regions from database.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/regions
```

## Records

Records endpoints

### 1. Create record

Create a new record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/regions/{{region_id}}/sites/{{site_id}}/records
```

**_Body:_**

```js
{
    "records_name":"string",
    "records_age":"integer",
    "records_sex":"string",
    "records_date_of_test_request":"date",
    "records_address":"string",
    "records_telephone":"string",
    "records_telephone_2":"string",
    "records_has_art_unique_code":"string",
    "records_art_unique_code":"string",
    "records_status":"string",
    "records_ward_bed_number":"string",
    "records_currently_pregnant":"string",
    "records_symptoms_current_cough":"boolean",
    "records_symptoms_fever":"boolean",
    "records_symptoms_night_sweats":"boolean",
    "records_symptoms_weight_loss":"boolean",
    "records_symptoms_none_of_the_above":"boolean",
    "records_patient_category_hospitalized":"boolean",
    "records_patient_category_child":"boolean",
    "records_patient_category_to_initiate_art":"boolean",
    "records_patient_category_on_art_symptomatic":"boolean",
    "records_patient_category_outpatient":"boolean",
    "records_patient_category_anc":"boolean",
    "records_patient_category_diabetes_clinic":"boolean",
    "records_patient_category_prisoner": "boolean",
    "records_patient_category_other":"string",
    "records_reason_for_test":"string",
    "records_reason_for_test_follow_up_months":"integer",
    "records_tb_treatment_history":"string",
    "records_tb_treatment_history_contact_of_tb_patient":"boolean",
    "records_tb_treatment_history_other": "string",
    "records_tb_type":"string",
    "records_tb_treatment_number":"string",
    "records_sms_notifications":"boolean",
    "records_requester_name": "string",
    "records_requester_telephone": "string"
}
```

### 2. Update record

Update a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/regions/{{region_id}}/sites/{{site_id}}/records/{{record_id}}
```

**_Body:_**

```js
{
    "records_name":"string",
    "records_age":"integer",
    "records_sex":"string",
    "records_date_of_test_request":"date",
    "records_address":"string",
    "records_telephone":"string",
    "records_telephone_2":"string",
    "records_has_art_unique_code":"string",
    "records_art_unique_code":"string",
    "records_status":"string",
    "records_ward_bed_number":"string",
    "records_currently_pregnant":"string",
    "records_symptoms_current_cough":"boolean",
    "records_symptoms_fever":"boolean",
    "records_symptoms_night_sweats":"boolean",
    "records_symptoms_weight_loss":"boolean",
    "records_symptoms_none_of_the_above":"boolean",
    "records_patient_category_hospitalized":"boolean",
    "records_patient_category_child":"boolean",
    "records_patient_category_to_initiate_art":"boolean",
    "records_patient_category_on_art_symptomatic":"boolean",
    "records_patient_category_outpatient":"boolean",
    "records_patient_category_anc":"boolean",
    "records_patient_category_diabetes_clinic":"boolean",
    "records_patient_category_prisoner": "boolean",
    "records_patient_category_other":"string",
    "records_reason_for_test":"string",
    "records_reason_for_test_follow_up_months":"integer",
    "records_tb_treatment_history":"string",
    "records_tb_treatment_history_contact_of_tb_patient":"boolean",
    "records_tb_treatment_history_other": "string",
    "records_tb_type":"string",
    "records_tb_treatment_number":"string",
    "records_sms_notifications":"boolean",
    "records_requester_name": "string",
    "records_requester_telephone": "string"
}
```

### 3. Fetch records

Fetch all records a user is permitted to access.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records
```

**_Query params:_**

| Key       | Value              | Description                        |
| --------- | ------------------ | ---------------------------------- |
| id        | <record_id>        | optional                           |
| site_id   | <record_site_id>   | required only when searching by ID |
| region_id | <record_region_id> | required only when searching by ID |
| name      | <record_name>      | optional                           |
| telephone | <record_telephone> | optional                           |

### 4. Fetch a record

Fetch a single record a user is permitted to access.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}
```

### 5. Create specimen collection

Create a new specimen collection for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/specimen_collections
```

**_Body:_**

```js
{
    "specimen_collection_1_date":"date",
    "specimen_collection_1_specimen_collection_type":"string",
    "specimen_collection_1_other":"string",
    "specimen_collection_1_period":"string",
    "specimen_collection_1_aspect":"string",
    "specimen_collection_1_received_by":"string",
    "specimen_collection_2_date":"string",
    "specimen_collection_2_specimen_collection_type":"string",
    "specimen_collection_2_other":"string",
    "specimen_collection_2_period":"string",
    "specimen_collection_2_aspect":"string",
    "specimen_collection_2_received_by":"string"
}
```

### 6. Update specimen collection

Update specimen collection for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/specimen_collections/{{specimen_collections_id}}
```

**_Body:_**

```js
{
    "specimen_collection_1_date":"date",
    "specimen_collection_1_specimen_collection_type":"string",
    "specimen_collection_1_other":"string",
    "specimen_collection_1_period":"string",
    "specimen_collection_1_aspect":"string",
    "specimen_collection_1_received_by":"string",
    "specimen_collection_2_date":"date",
    "specimen_collection_2_specimen_collection_type":"string",
    "specimen_collection_2_other":"string",
    "specimen_collection_2_period":"string",
    "specimen_collection_2_aspect":"string",
    "specimen_collection_2_received_by":"string"
}
```

### 7. Fetch specimen collections

Fetch specimen collections for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/specimen_collections
```

### 8. Create lab

Create a new labs for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/labs
```

**_Body:_**

```js
{
    "lab_date_specimen_collection_received":"date",
    "lab_received_by":"string",
    "lab_registration_number":"string",
    "lab_smear_microscopy_result_result_1":"string",
    "lab_smear_microscopy_result_result_2":"string",
    "lab_smear_microscopy_result_date":"date",
    "lab_smear_microscopy_result_done_by":"string",
    "lab_xpert_mtb_rif_assay_result":"string",
    "lab_xpert_mtb_rif_assay_grades":"string",
    "lab_xpert_mtb_rif_assay_rif_result":"string",
    "lab_xpert_mtb_rif_assay_result_2":"string",
    "lab_xpert_mtb_rif_assay_grades_2":"string",
    "lab_xpert_mtb_rif_assay_rif_result_2":"string",
    "lab_xpert_mtb_rif_assay_date":"date",
    "lab_xpert_mtb_rif_assay_done_by":"string",
    "lab_urine_lf_lam_result":"string",
    "lab_urine_lf_lam_date":"date",
    "lab_urine_lf_lam_done_by":"string",
    "lab_culture_mgit_culture":"string",
    "lab_culture_lj_culture":"string",
    "lab_culture_date":"date",
    "lab_culture_done_by":"string",
    "lab_lpa_mtbdrplus_isoniazid":"string",
    "lab_lpa_mtbdrplus_rifampin":"string",
    "lab_lpa_mtbdrs_flouoroquinolones":"string",
    "lab_lpa_mtbdrs_kanamycin":"string",
    "lab_lpa_mtbdrs_amikacin":"string",
    "lab_lpa_mtbdrs_capreomycin":"string",
    "lab_lpa_mtbdrs_low_level_kanamycin":"string",
    "lab_lpa_date":"date",
    "lab_lpa_done_by":"string",
    "lab_dst_isonazid":"string",
    "lab_dst_rifampin":"string",
    "lab_dst_ethambutol":"string",
    "lab_dst_kanamycin":"string",
    "lab_dst_ofloxacin":"string",
    "lab_dst_levofloxacinekanamycin":"string",
    "lab_dst_moxifloxacinekanamycin":"string",
    "lab_dst_amikacinekanamycin":"string",
    "lab_dst_date":"date",
    "lab_dst_done_by":"string",
    "lab_result_type":"string"
}
```

### 9. Update lab

Update labs for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/labs/{{labs_id}}
```

**_Body:_**

```js
{
    "lab_date_specimen_collection_received":"date",
    "lab_received_by":"string",
    "lab_registration_number":"string",
    "lab_smear_microscopy_result_result_1":"string",
    "lab_smear_microscopy_result_result_2":"string",
    "lab_smear_microscopy_result_date":"date",
    "lab_smear_microscopy_result_done_by":"string",
    "lab_xpert_mtb_rif_assay_result":"string",
    "lab_xpert_mtb_rif_assay_grades":"string",
    "lab_xpert_mtb_rif_assay_rif_result":"string",
    "lab_xpert_mtb_rif_assay_result_2":"string",
    "lab_xpert_mtb_rif_assay_grades_2":"string",
    "lab_xpert_mtb_rif_assay_rif_result_2":"string",
    "lab_xpert_mtb_rif_assay_date":"date",
    "lab_xpert_mtb_rif_assay_done_by":"string",
    "lab_urine_lf_lam_result":"string",
    "lab_urine_lf_lam_date":"date",
    "lab_urine_lf_lam_done_by":"string",
    "lab_culture_mgit_culture":"string",
    "lab_culture_lj_culture":"string",
    "lab_culture_date":"date",
    "lab_culture_done_by":"string",
    "lab_lpa_mtbdrplus_isoniazid":"string",
    "lab_lpa_mtbdrplus_rifampin":"string",
    "lab_lpa_mtbdrs_flouoroquinolones":"string",
    "lab_lpa_mtbdrs_kanamycin":"string",
    "lab_lpa_mtbdrs_amikacin":"string",
    "lab_lpa_mtbdrs_capreomycin":"string",
    "lab_lpa_mtbdrs_low_level_kanamycin":"string",
    "lab_lpa_date":"date",
    "lab_lpa_done_by":"string",
    "lab_dst_isonazid":"string",
    "lab_dst_rifampin":"string",
    "lab_dst_ethambutol":"string",
    "lab_dst_kanamycin":"string",
    "lab_dst_ofloxacin":"string",
    "lab_dst_levofloxacinekanamycin":"string",
    "lab_dst_moxifloxacinekanamycin":"string",
    "lab_dst_amikacinekanamycin":"string",
    "lab_dst_date":"date",
    "lab_dst_done_by":"string",
    "lab_result_type":"string"
}
```

### 10. Fetch labs

Fetch labs for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/labs
```

### 11. Create follow up

Create a new follow-up for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/follow_ups
```

**_Body:_**

```js
{
    "follow_up_xray":"boolean",
    "follow_up_amoxicillin":"boolean",
    "follow_up_other_antibiotic":"string",
    "follow_up_schedule_date":"date",
    "follow_up_comments":"string"
}
```

### 12. Update follow up

Update follow-up for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/follow_ups/{{follow_ups_id}}
```

**_Body:_**

```js
{
    "follow_up_xray":"boolean",
    "follow_up_amoxicillin":"boolean",
    "follow_up_other_antibiotic":"string",
    "follow_up_schedule_date":"date",
    "follow_up_comments":"string"
}
```

### 13. Fetch follow ups

Fetch follow-ups for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/follow_ups
```

### 14. Create outcome recorded

Create a new outcome recorded for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/outcome_recorded
```

**_Body:_**

```js
{
    "outcome_recorded_started_tb_treatment_outcome":"string",
    "outcome_recorded_tb_rx_number":"string",
    "outcome_recorded_other":"string",
    "outcome_recorded_comments":"string"
}
```

### 15. Update outcome recorded

Update outcome recorded for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/outcome_recorded/{{outcome_recorded_id}}
```

**_Body:_**

```js
{
    "outcome_recorded_started_tb_treatment_outcome":"string",
    "outcome_recorded_tb_rx_number":"string",
    "outcome_recorded_other":"string",
    "outcome_recorded_comments":"string"
}
```

### 16. Fetch outcome recorded

Fetch outcome recorded for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/outcome_recorded
```

### 17. Create tb treatment outcome

Create a new tb treatment outcome for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: POST
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/tb_treatment_outcomes
```

**_Body:_**

```js
{
    "tb_treatment_outcome_result":"string",
    "tb_treatment_outcome_comments":"string",
    "tb_treatment_outcome_close_patient_file":"string"
}
```

### 18. Update tb treatment outcome

Update tb treatment outcome for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: PUT
Content-Type: application/json
URL: {{domain}}/v1/tb_treatment_outcomes/{{tb_treatment_outcomes_id}}
```

**_Body:_**

```js
{
    "tb_treatment_outcome_result":"string",
    "tb_treatment_outcome_comments":"string",
    "tb_treatment_outcome_close_patient_file":"boolean"
}
```

### 19. Fetch tb treatment outcomes

Fetch tb treatment outcomes for a record.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/records/{{record_id}}/tb_treatment_outcomes
```

## Exports

Exports endpoint

### 1. Export data

Export data permitted to access.

**_Responses:_**

- `200` - OK
- `400` - Bad Request
- `401` - Unauthorised
- `403` - Forbidden
- `500` - Internal Server Error

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/regions/{{region_id}}/sites/{{site_id}}/exports/{{export_type}}
```

**_Query params:_**

| Key        | Value  | Description |
| ---------- | ------ | ----------- |
| start_date | <date> |             |
| end_date   | <date> |             |

---

[Back to top](#chpr-is-api-references)
