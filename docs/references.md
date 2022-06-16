# CHPR-IS API References

Manage Users, Sites and Records endpoints

## Endpoints

- [Users](#users)
  1. [Signup](#1-signup)
  1. [Login](#2-login)
  1. [Fetch profile](#3-fetch-profile)
  1. [Update profile](#4-update-profile)
  1. [Fetch all users](#5-fetch-all-users)
  1. [Fetch a user](#6-fetch-a-user)
  1. [Update a user](#7-update-a-user)
  1. [Update account status](#8-update-account-status)
  1. [Update password](#9-update-password)
  1. [Add sites](#10-add-sites)
  1. [Remove sites](#11-remove-sites)
- [Sites](#sites)
  1. [Create site](#1-create-site)
  1. [Fetch all sites](#2-fetch-all-sites)
  1. [Create region](#3-create-region)
  1. [Fetch all regions](#4-fetch-all-regions)
- [Records](#records)
  1. [Create record](#1-create-record)
  1. [Fetch records](#2-fetch-records)
  1. [Create specimen collection](#3-create-specimen-collection)
  1. [Fetch specimen collections](#4-fetch-specimen-collections)
  1. [Create lab](#5-create-lab)
  1. [Fetch labs](#6-fetch-labs)
  1. [Create follow up](#7-create-follow-up)
  1. [Fetch follow ups](#8-fetch-follow-ups)
  1. [Create outcome recorded](#9-create-outcome-recorded)
  1. [Fetch outcome recorded](#10-fetch-outcome-recorded)
  1. [Create tb treatment outcome](#11-create-tb-treatment-outcome)
  1. [Fetch tb treatment outcomes](#12-fetch-tb-treatment-outcomes)
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
    "site_id": "integer"
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

### 3. Fetch profile

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

### 4. Update profile

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
    "occupation": "string"
}
```

### 5. Fetch all users

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

### 6. Fetch a user

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

### 7. Update a user

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

### 8. Update account status

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

### 9. Update password

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

### 10. Add sites

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

### 11. Remove sites

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

### 2. Fetch all sites

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

### 3. Create region

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
    "name": "string"
}
```

### 4. Fetch all regions

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
    "records_patient_category_other":"string",
    "records_reason_for_test_presumptive_tb":"boolean",
    "records_tb_treatment_history":"string",
    "records_tb_treatment_history_contact_of_tb_patient":"string"
}
```

### 2. Fetch records

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

### 3. Create specimen collection

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

### 4. Fetch specimen collections

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

### 5. Create lab

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
    "lab_smear_microscopy_result_date":"string",
    "lab_smear_microscopy_result_done_by":"string",
    "lab_xpert_mtb_rif_assay_result":"string",
    "lab_xpert_mtb_rif_assay_grades":"string",
    "lab_xpert_mtb_rif_assay_rif_result":"string",
    "lab_xpert_mtb_rif_assay_date":"string",
    "lab_xpert_mtb_rif_assay_done_by":"string",
    "lab_urine_lf_lam_result":"string",
    "lab_urine_lf_lam_date":"string",
    "lab_urine_lf_lam_done_by":"string"
}
```

### 6. Fetch labs

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

### 7. Create follow up

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

### 8. Fetch follow ups

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

### 9. Create outcome recorded

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

### 10. Fetch outcome recorded

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

### 11. Create tb treatment outcome

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

### 12. Fetch tb treatment outcomes

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

**_Endpoint:_**

```bash
Method: GET
Content-Type: application/json
URL: {{domain}}/v1/regions/{{region_id}}/sites/{{site_id}}/exports/{{export_type}}?start_date=<date>&end_date=<date>
```

**_Query params:_**

| Key        | Value  | Description |
| ---------- | ------ | ----------- |
| start_date | <date> |             |
| end_date   | <date> |             |

---

[Back to top](#chpr-is-api-references)
