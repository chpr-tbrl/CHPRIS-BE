# Tests

### Create new record

> Request

```bash
curl --location --request POST 'http://localhost:9000/v1/users/0/sites/0/regions/0/records' \
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
> - `500` = Error occurred

### Fetch records for user

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users/0/sites/0/regions/0/records' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred

### Fetch all users

> Request

```bash
curl --location --request GET 'http://localhost:9000/v1/users' \
--data-raw ''
```

> Response
>
> - `200` = Success
> - `500` = Error occurred
