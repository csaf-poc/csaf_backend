# CSAF Backend API

Based on this work, a [CSAF Content Management System](https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html#916-conformance-clause-6-csaf-content-management-system) is developed at [Secvisogram/CSAF-CMS-Backend](https://github.com/secvisogram/csaf-cms-backend). This PoC is not longer maintained.

## Architecture
![Architecture](https://github.com/pdamian/csaf_backend/blob/main/Architecture_CSAF-Backend.png)

## Installation
First, clone the project:
```
git clone https://github.com/pdamian/csaf_backend.git && cd csaf_backend/
```
Then, create a file named `.env` that stores your secrets (update with your own set of values):
```
cat << EOF > .env
# Keycloak IDP
KEYCLOAK_USER="<KEYCLOAK_ADMIN_USER>"
KEYCLOAK_PASSWORD="<KEYCLOAK_ADMIN_PASSWORD>"
KEYCLOAK_DB_USER="<KEYCLOAK_DB_USER>"
KEYCLOAK_DB_PASSWORD="<KEYCLOAK_DB_PASSWORD>"

# Keycloak OIDC
OIDC_PROVIDER="http://<IP-OPENID_PROVIDER>:8080"        # OpenID Provider
OIDC_CLIENT_SECRET="<CLIENT_SECRET>"                    # Client Secret
OIDC_REDIRECT_URIS="*"                                  # Comma-separated redirect URIs

# CSAF API Database
MONGO_ROOT="<MONGODB_ADMIN_USER>"
MONGO_ROOT_PASSWORD="<MONGODB_ADMIN_PASSWORD>"
MONGO_USER="<MONGODB_USER>"
MONGO_USER_PASSWORD="<MONGODB_PASSWORD>"
EOF
```
### Requirements
Ensure that you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

The development setup further requires the packages `python3` and `python3-venv` being installed.
### Setup
Start the containers either for testing or development. Note that both setups are not recommended to be used in production.
#### Testing
Launch the containers:
```
docker-compose -f docker-compose.test.yml up -d
```
After a while, the Keycloak IdP and CSAF Backend API specification should become accessible at:
```
curl http://localhost:8080/
curl http://localhost:5000/api/specs/
```
If needed, the containers can be stopped with (add `--volumes` to drop all persisted data, e.g. users added to Keycloak or stored advisories):
```
docker-compose -f docker-compose.test.yml down
```
#### Development
Launch the containers:
```
docker-compose -f docker-compose.dev.yml up -d
```
Manually launch the CSAF backend API:
```
# Environment variables
export $(cat .env | sed -E 's/#.*$|//g' | xargs)
export FLASK_ENV=development

# Python virtual environment
python3 -mvenv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt

# Flask server
flask run --host=0.0.0.0
```
After a while, the Keycloak IdP and CSAF Backend API specification should become accessible at:
```
curl http://localhost:8080/
curl http://localhost:5000/api/specs/
```
If needed, the containers can be stopped with (add `--volumes` to drop all persisted data, e.g. users added to Keycloak or stored advisories):
```
docker-compose -f docker-compose.dev.yml down
```
Use the following commands if you want to unset the previously configured environment variables:
```
unset $(cat .env | sed -E 's/#.*$|\=.*$//g' | xargs)
unset FLASK_ENV
```
## How To
### Keycloak Test User
1. Using a web browser, access and login to the [Keycloak Administration Console](http://localhost:8080/auth/) (use your specified secrets)
3. Select the `CSAF` realm, and go to `Manage/Users`
4. Click `Add User`
5. Enter a `Username` and click `Save`
6. Switch to the `Credentials` tab, enter a `Password` and `Password Confirmation` and click `Set Password`
### CSAF Backend API Test
1. Simulate a Keycloak user login to receive an access token for the Backend API:
```
curl -L -X POST 'http://<KEYCLOAK_IP>:8080/auth/realms/CSAF/protocol/openid-connect/token' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        --data-urlencode 'client_id=csaf-client' \
        --data-urlencode 'grant_type=password' \
        --data-urlencode 'client_secret=<CLIENT_SECRET>' \
        --data-urlencode 'scope=openid' \
        --data-urlencode 'username=<USER>' \
        --data-urlencode 'password=<PASSWORD>'
```
2. Use the access token to query the CSAF Backend API:
```
curl -L -X GET 'http://<CSAF_BACKEND_IP>:5000/api/advisories' -H 'Authorization: Bearer <ACCESS_TOKEN>'
```
Note: The access token can also be used at the [CSAF Backend API specification](http://<CSAF_BACKEND_IP>:5000/api/specs/).
## Note
This project was developed by the [armasuisse Cyber-Defense Campus](https://www.ar.admin.ch/en/armasuisse-wissenschaft-und-technologie-w-t/cyber-defence_campus.html).
