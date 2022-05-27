# Features

## Table of contents

1. [Create an account](#1-create-an-account)
2. [Authenticate an account](#2-authenticate-an-account)
3. [Fetch Users](#3-fetch-users)
4. [Create Records](#4-create-records)
5. [Fetch Records](#5-fetch-records)
6. [Create specimen collection records](#6-create-specimen-collection-records)
7. [Fetch specimen collection records](#7-fetch-specimen-collection-records)
8. [Create lab records](#8-create-lab-records)
9. [Fetch lab records](#9-fetch-lab-records)
10. [Create follow up records](#10-create-follow-up-records)
11. [Fetch follow up records](#11-fetch-follow-up-records)
12. [Create outcome recorded records](#12-create-outcome-recorded-records)
13. [Fetch outcome recorded records](#13-fetch-outcome-recorded-records)
14. [Create tb treatment outcome records](#14-create-tb-treatment-outcome-records)
15. [Fetch tb treatment outcome records](#15-fetch-tb-treatment-outcome-records)
16. [Update Users](#16-update-users)
17. [Create regions](#17-create-regions)
18. [Fetch regions](#18-fetch-regions)
19. [Create sites](#19-create-sites)
20. [Fetch sites](#20-fetch-sites)
21. [Fetch Users](#21-fetch-a-user)

## 1. Create an account

Using the REST User management API, a new user can be added to the CHPR-IS database.

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- Email
- Phone Number
- Name
- Region
- Site
- Occupation
- Password

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"",
    "name": "",
    "email": "",
    "password": "",
    "occupation": "",
    "site_id": "",
    "region_id": ""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a dict

- uid

```bash
{
    "uid": ""
}
```

## 2. Authenticate an account

Authentication is the process whereby a user provides their credentials for identification to obtain adequate resources.

### 1. With email

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- Email
- Password

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "",
    "password": ""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a dict

- uid

```bash
{
    "uid": ""
}
```

## 3. Fetch users

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/users' \
--header 'Content-Type: application/json' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "createdAt": "",
        "email": "",
        "id": "",
        "name": "",
        "occupation": "",
        "phone_number": "",
        "region_id": "",
        "site_id": "",
        "state": "",
        "type_of_export": "",
        "type_of_user": "",
        "exportable_range": ""
    }
]
```

## 4. Create records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- records_name
- records_age
- records_sex
- records_date_of_test_request
- records_address
- records_telephone
- records_telephone_2
- records_has_art_unique_code
- records_art_unique_code
- records_status
- records_ward_bed_number
- records_currently_pregnant
- records_symptoms_current_cough
- records_symptoms_fever
- records_symptoms_night_sweats
- records_symptoms_weight_loss
- records_symptoms_none_of_the_above
- records_patient_category_hospitalized
- records_patient_category_child
- records_patient_category_to_initiate_art
- records_patient_category_on_art_symptomatic
- records_patient_category_outpatient
- records_patient_category_anc
- records_patient_category_diabetes_clinic
- records_patient_category_other
- records_reason_for_test_presumptive_tb
- records_tb_treatment_history
- records_tb_treatment_history_contact_of_tb_patient

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records' \
--header 'Content-Type: application/json' \
--data-raw '{
    "records_name":"",
    "records_age":1,
    "records_sex":"",
    "records_date_of_test_request":"",
    "records_address":"",
    "records_telephone":"",
    "records_telephone_2":"",
    "records_has_art_unique_code":"",
    "records_art_unique_code":"",
    "records_status":"",
    "records_ward_bed_number":"",
    "records_currently_pregnant":"",
    "records_symptoms_current_cough":"",
    "records_symptoms_fever":"",
    "records_symptoms_night_sweats":"",
    "records_symptoms_weight_loss":"",
    "records_symptoms_none_of_the_above":"",
    "records_patient_category_hospitalized":"",
    "records_patient_category_child":"",
    "records_patient_category_to_initiate_art":"",
    "records_patient_category_on_art_symptomatic":"",
    "records_patient_category_outpatient":"",
    "records_patient_category_anc":"",
    "records_patient_category_diabetes_clinic":"",
    "records_patient_category_other":"",
    "records_reason_for_test_presumptive_tb":"",
    "records_tb_treatment_history":"",
    "records_tb_treatment_history_contact_of_tb_patient":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 5. Fetch records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "record_id":"",
        "records_date":"",
        "site_id":"",
        "region_id":"",
        "records_user_id":"",
        "records_name":"",
        "records_age":"",
        "records_sex":"",
        "records_date_of_test_request":"",
        "records_address":"",
        "records_telephone":"",
        "records_telephone_2":"",
        "records_has_art_unique_code":"",
        "records_art_unique_code":"",
        "records_status":"",
        "records_ward_bed_number":"",
        "records_currently_pregnant":"",
        "records_symptoms_current_cough":"",
        "records_symptoms_fever":"",
        "records_symptoms_night_sweats":"",
        "records_symptoms_weight_loss":"",
        "records_symptoms_none_of_the_above":"",
        "records_patient_category_hospitalized":"",
        "records_patient_category_child":"",
        "records_patient_category_to_initiate_art":"",
        "records_patient_category_on_art_symptomatic":"",
        "records_patient_category_outpatient":"",
        "records_patient_category_anc":"",
        "records_patient_category_diabetes_clinic":"",
        "records_patient_category_other":"",
        "records_reason_for_test_presumptive_tb":"",
        "records_tb_treatment_history":"",
        "records_tb_treatment_history_contact_of_tb_patient":"",
    }
]
```

## 6. Create specimen collection records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- specimen_collection_1_date
- specimen_collection_1_specimen_collection_type
- specimen_collection_1_other
- specimen_collection_1_period
- specimen_collection_1_aspect
- specimen_collection_1_received_by
- specimen_collection_2_date
- specimen_collection_2_specimen_collection_type
- specimen_collection_2_other
- specimen_collection_2_period
- specimen_collection_2_aspect
- specimen_collection_2_received_by

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/specimen_collections' \
--header 'Content-Type: application/json' \
--data-raw '{
    "specimen_collection_1_date":"",
    "specimen_collection_1_specimen_collection_type":"",
    "specimen_collection_1_other":"",
    "specimen_collection_1_period":"",
    "specimen_collection_1_aspect":"",
    "specimen_collection_1_received_by":"",
    "specimen_collection_2_date":"",
    "specimen_collection_2_specimen_collection_type":"",
    "specimen_collection_2_other":"",
    "specimen_collection_2_period":"",
    "specimen_collection_2_aspect":"",
    "specimen_collection_2_received_by":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 7. Fetch specimen collection records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/specimen_collections' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "specimen_collection_1_aspect":"",
        "specimen_collection_1_date":"",
        "specimen_collection_1_other":"",
        "specimen_collection_1_period":"",
        "specimen_collection_1_received_by":"",
        "specimen_collection_1_specimen_collection_type":"",
        "specimen_collection_2_aspect":"",
        "specimen_collection_2_date":"",
        "specimen_collection_2_other":"",
        "specimen_collection_2_period":"",
        "specimen_collection_2_received_by":"",
        "specimen_collection_2_specimen_collection_type":"",
        "specimen_collection_date":"",
        "specimen_collection_id":"",
        "specimen_collection_records_id":"",
        "specimen_collection_user_id":"",
    }
]
```

## 8. Create lab records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- lab_date_specimen_collection_received
- lab_received_by
- lab_registration_number
- lab_smear_microscopy_result_result_1
- lab_smear_microscopy_result_result_2
- lab_smear_microscopy_result_date
- lab_smear_microscopy_result_done_by
- lab_xpert_mtb_rif_assay_result
- lab_xpert_mtb_rif_assay_grades
- lab_xpert_mtb_rif_assay_rif_result
- lab_xpert_mtb_rif_assay_date
- lab_xpert_mtb_rif_assay_done_by
- lab_urine_lf_lam_result
- lab_urine_lf_lam_date
- lab_urine_lf_lam_done_by

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/labs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lab_date_specimen_collection_received":"",
    "lab_received_by":"",
    "lab_registration_number":"",
    "lab_smear_microscopy_result_result_1":"",
    "lab_smear_microscopy_result_result_2":"",
    "lab_smear_microscopy_result_date":"",
    "lab_smear_microscopy_result_done_by":"",
    "lab_xpert_mtb_rif_assay_result":"",
    "lab_xpert_mtb_rif_assay_grades":"",
    "lab_xpert_mtb_rif_assay_rif_result":"",
    "lab_xpert_mtb_rif_assay_date":"",
    "lab_xpert_mtb_rif_assay_done_by":"",
    "lab_urine_lf_lam_result":"",
    "lab_urine_lf_lam_date":"",
    "lab_urine_lf_lam_done_by":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 9. Fetch lab records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/labs' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "lab_date":"",
        "lab_date_specimen_collection_received":"",
        "lab_id":"",
        "lab_received_by":"",
        "lab_records_id":"",
        "lab_registration_number":"",
        "lab_smear_microscopy_result_date":"",
        "lab_smear_microscopy_result_done_by":"",
        "lab_smear_microscopy_result_result_1":"",
        "lab_smear_microscopy_result_result_2":"",
        "lab_urine_lf_lam_date":"",
        "lab_urine_lf_lam_done_by":"",
        "lab_urine_lf_lam_result":"",
        "lab_user_id":"",
        "lab_xpert_mtb_rif_assay_date":"",
        "lab_xpert_mtb_rif_assay_done_by":"",
        "lab_xpert_mtb_rif_assay_grades":"",
        "lab_xpert_mtb_rif_assay_result":"",
        "lab_xpert_mtb_rif_assay_rif_result":""
    }
]
```

## 10. Create follow up records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- follow_up_xray
- follow_up_amoxicillin
- follow_up_other_antibiotic
- follow_up_schedule_date
- follow_up_comments

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/follow_ups' \
--header 'Content-Type: application/json' \
--data-raw '{
    "follow_up_xray":"",
    "follow_up_amoxicillin":"",
    "follow_up_other_antibiotic":"",
    "follow_up_schedule_date":"",
    "follow_up_comments":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 11. Fetch follow up records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/follow_ups' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "follow_up_amoxicillin": "",
        "follow_up_comments": "",
        "follow_up_date": "",
        "follow_up_id": "",
        "follow_up_other_antibiotic": "",
        "follow_up_records_id": 1,
        "follow_up_schedule_date": "",
        "follow_up_user_id": "",
        "follow_up_xray": ""
    }
]
```

## 12. Create outcome recorded records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- outcome_recorded_started_tb_treatment_outcome
- outcome_recorded_tb_rx_number
- outcome_recorded_other
- outcome_recorded_comments

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/outcome_recorded' \
--header 'Content-Type: application/json' \
--data-raw '{
    "outcome_recorded_started_tb_treatment_outcome":"",
    "outcome_recorded_tb_rx_number":"",
    "outcome_recorded_other":"",
    "outcome_recorded_comments":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 13. Fetch outcome recorded records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/outcome_recorded' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "outcome_recorded_comments": "",
        "outcome_recorded_date": "",
        "outcome_recorded_id": "",
        "outcome_recorded_other": "",
        "outcome_recorded_records_id": "",
        "outcome_recorded_started_tb_treatment_outcome": "",
        "outcome_recorded_tb_rx_number": "",
        "outcome_recorded_user_id": ""
    }
]
```

## 14. Create tb treatment outcome records

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- outcome_recorded_started_tb_treatment_outcome
- outcome_recorded_tb_rx_number
- outcome_recorded_other
- outcome_recorded_comments

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/tb_treatment_outcomes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tb_treatment_outcome_result":"",
    "tb_treatment_outcome_comments":"",
    "tb_treatment_outcome_close_patient_file":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 15. Fetch tb treatment outcome records

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>/records/<record_id>/tb_treatment_outcomes' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "tb_treatment_outcome_close_patient_file": "",
        "tb_treatment_outcome_comments": "",
        "tb_treatment_outcome_date": "",
        "tb_treatment_outcome_id": "",
        "tb_treatment_outcome_records_id": "",
        "tb_treatment_outcome_result": "",
        "tb_treatment_outcome_user_id": ""
    }
]
```

## 16. Update Users

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- phone_number
- name
- email
- password
- occupation
- site_id
- region_id
- state
- type_of_export
- type_of_user

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request PUT 'http://localhost:9000/v1/admin/users/<user_id>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"",
    "name": "",
    "email": "",
    "password": "",
    "occupation": "",
    "site_id": "",
    "region_id":"",
    "state":"",
    "type_of_export": "",
    "type_of_user":"",
    "exportable_range":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 17. Create regions

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- name

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/admin/regions' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 18. Fetch regions

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/regions' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "createdAt": "",
        "id": "",
        "name": ""
    }
]
```

## 19. Create sites

The user has to provide the following in the [request body](https://developer.mozilla.org/en-US/docs/Web/API/Request/body):

- name

The user also must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request POST 'http://localhost:9000/v1/admin/regions/<region_id>/sites' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":""
}'
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200`.

## 20. Fetch sites

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/regions/<region_id>/sites' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "createdAt": "",
        "id": "",
        "name": "",
        "region_id":""
    }
]
```

## 21. Fetch a user

The user must configure their [header](https://developer.mozilla.org/en-US/docs/Glossary/Representation_header) to:

- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) = application/json

Here is an example. Running User management API locally on port 9000

```bash
curl --location --request GET 'http://localhost:9000/v1/users/<user_id>' \
--data-raw ''
```

If successful, the response should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain a list

- []

```bash
[
    {
        "createdAt": "",
        "email": "",
        "id": "",
        "name": "",
        "occupation": "",
        "phone_number": "",
        "region_id": "",
        "site_id": "",
        "state": "",
        "type_of_export": "",
        "type_of_user": "",
        "exportable_range": ""
    }
]
```
