# References

## APIv1 end-points

### Authentication

| Action                                                                | Endpoint            | Parameters | Request body                                                                                                                                                                             |
| :-------------------------------------------------------------------- | :------------------ | :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Create an account](./features_v1.md#1-create-an-account)             | **POST** /v1/signup | None       | <ul><li>phone_number = STRING</li><li>name = STRING</li><li>email = STRING</li><li>password = STRING</li><li>occupation = STRING</li><li>site = STRING</li><li>region = STRING</li></ul> |
| [Authenticate an account](./features_v1.md#2-authenticate-an-account) | **POST** /v1/login  | None       | <ul><li>email = STRING</li><li>password = STRING</li></ul>                                                                                                                               |

### Users

| Action                                        | Endpoint          | Parameters | Request body |
| :-------------------------------------------- | :---------------- | :--------- | :----------- |
| [Fetch Users](./features_v1.md#3-fetch-users) | **GET** /v1/users | None       | None         |
