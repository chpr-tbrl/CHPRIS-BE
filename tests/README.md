# Tests

### Signup

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"+xxx-xxx-xxx",
    "name": "username",
    "email": "example@mail.com",
    "password": "password",
    "occupation": "occupation",
    "site_id": 1,
    "region_id": 1
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `409` = Conflict
> - `500` = Error occurred

### Login

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "example@mail.com",
    "password": "password"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `409` = Conflict
> - `500` = Error occurred

### Fetch all users

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/users' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Create new record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records' \
--header 'Content-Type: application/json' \
--data-raw '{
    "records_name":"sample",
    "records_age":1,
    "records_sex":"female",
    "records_date_of_test_request":"2022-05-17",
    "records_address":"address",
    "records_telephone":"123456789",
    "records_telephone_2":null,
    "records_has_art_unique_code":"yes",
    "records_art_unique_code":"1234",
    "records_status":"ward-bed",
    "records_ward_bed_number":"12",
    "records_currently_pregnant":"no",
    "records_symptoms_current_cough":false,
    "records_symptoms_fever":false,
    "records_symptoms_night_sweats":false,
    "records_symptoms_weight_loss":false,
    "records_symptoms_none_of_the_above":false,
    "records_patient_category_hospitalized":false,
    "records_patient_category_child":false,
    "records_patient_category_to_initiate_art":false,
    "records_patient_category_on_art_symptomatic":false,
    "records_patient_category_outpatient":false,
    "records_patient_category_anc":false,
    "records_patient_category_diabetes_clinic":false,
    "records_patient_category_other":null,
    "records_reason_for_test_presumptive_tb":true,
    "records_tb_treatment_history":"relapse",
    "records_tb_treatment_history_contact_of_tb_patient":null
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `500` = Error occurred

### Fetch records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `401` = Unauthorized
> - `500` = Error occurred

### Create new specimen_collection record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records/1/specimen_collections' \
--header 'Content-Type: application/json' \
--data-raw '{
    "specimen_collection_1_date":"2022-05-17",
    "specimen_collection_1_specimen_collection_type":"sputum",
    "specimen_collection_1_other":"text",
    "specimen_collection_1_period":"morning",
    "specimen_collection_1_aspect":"bloody",
    "specimen_collection_1_received_by":"text",
    "specimen_collection_2_date":"2022-05-17",
    "specimen_collection_2_specimen_collection_type":"csf",
    "specimen_collection_2_other":"text",
    "specimen_collection_2_period":"morning",
    "specimen_collection_2_aspect":"salivary",
    "specimen_collection_2_received_by":"text"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `500` = Error occurred

### Fetch specimen_collection records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records/1/specimen_collections' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `401` = Unauthorized
> - `500` = Error occurred

### Create new lab record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records/1/labs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lab_date_specimen_collection_received":"2022-05-17",
    "lab_received_by":"text",
    "lab_registration_number":"text",
    "lab_smear_microscopy_result_result_1":"1+",
    "lab_smear_microscopy_result_result_2":"2+",
    "lab_smear_microscopy_result_date":"2022-05-17",
    "lab_smear_microscopy_result_done_by":"text",
    "lab_xpert_mtb_rif_assay_result":"trace",
    "lab_xpert_mtb_rif_assay_grades":"low",
    "lab_xpert_mtb_rif_assay_rif_result":"not_done",
    "lab_xpert_mtb_rif_assay_date":"2022-05-17",
    "lab_xpert_mtb_rif_assay_done_by":"text",
    "lab_urine_lf_lam_result":"positive",
    "lab_urine_lf_lam_date":"2022-05-17",
    "lab_urine_lf_lam_done_by":"text"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `500` = Error occurred

### Fetch lab records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records/1/labs' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Create new follow_up record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records/1/follow_ups' \
--header 'Content-Type: application/json' \
--data-raw '{
    "follow_up_xray":true,
    "follow_up_amoxicillin":false,
    "follow_up_other_antibiotic":null,
    "follow_up_schedule_date":"2022-05-19",
    "follow_up_comments":"text"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `500` = Error occurred

### Fetch follow_up records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records/1/follow_ups' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Create new outcome_recorded record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records/1/outcome_recorded' \
--header 'Content-Type: application/json' \
--data-raw '{
    "outcome_recorded_started_tb_treatment_outcome":"started_tb_treatment",
    "outcome_recorded_tb_rx_number":"text",
    "outcome_recorded_other":null,
    "outcome_recorded_comments":"text"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `500` = Error occurred

### Fetch outcome_recorded records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records/1/outcome_recorded' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Create new tb_treatment_outcome record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/1/records/1/tb_treatment_outcomes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tb_treatment_outcome_result":"cured",
    "tb_treatment_outcome_comments":"text",
    "tb_treatment_outcome_close_patient_file":true
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `500` = Error occurred

### Fetch tb_treatment_outcome records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1/records/1/tb_treatment_outcomes' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Update a user's account

> Request

```bash
curl --location --request PUT 'http://localhost:9000/v1/admin/users/1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"+xxx-xxx-xxx",
    "name": "username",
    "email": "example@mail.com",
    "password": "password",
    "occupation": "occupation",
    "site_id": 1,
    "region_id":1,
    "state":"verified",
    "type_of_export": null,
    "type_of_user":"admin",
    "exportable_range":1
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `500` = Error occurred

### Create new region

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/admin/regions' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "region"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `409` = Conflict
> - `500` = Error occurred

### Fetch all regions

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/regions' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Create new site

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/admin/regions/1/sites' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "site"
}'
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `409` = Conflict
> - `500` = Error occurred

### Fetch all regions

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/admin/regions/1/sites' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Fetch a user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/1' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `400` = Bad request
> - `401` = Unauthorized
> - `500` = Error occurred
