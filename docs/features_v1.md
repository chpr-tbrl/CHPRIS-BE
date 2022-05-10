# Features

## Table of contents

1. [Create an account](#1-create-an-account)
2. [Authenticate an account](#2-authenticate-an-account)

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
    "phone_number":"+xxx-xxx-xxx",
    "name": "username",
    "email": "example@mail.com",
    "password": "password",
    "occupation": "occupation",
    "site": "site",
    "region": "region"
}'
```

If successful a [cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cookie) is set on the user's agent valid for two hours. The cookie is used to track the user's seesion. Also the [response](https://developer.mozilla.org/en-US/docs/Web/API/Response/body) should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain

- uid

```bash
{
    "uid": "xxxxxxxxxxxxxx"
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
    "email": "example@mail.com",
    "password": "password"
}'
```

If successful a [cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cookie) is set on the user's agent valid for two hours. The cookie is used to track the user's seesion. Also the [response](https://developer.mozilla.org/en-US/docs/Web/API/Response/body) should have a [status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of `200` and the body should contain

- uid

```bash
{
    "uid": "xxxxxx-xxxx-xxxx-xxxx-xxxxxx"
}
```
