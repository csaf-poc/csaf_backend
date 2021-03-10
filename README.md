# csaf_backend
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
Start the containers either for testing or development.
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
export $(cat .env | grep -v -E '#.*$' | xargs)
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

# TODO: Remove
## Notes
### Test Setup
The following commands can be used for testing the CSAF backend. Note that the corresponding database is not presisted and accesses done by the DB root user. This setup is not recommended for production purposes.
```
$ cd csaf_backend/
$ docker-compose -f docker-compose.test.yml up -d
$ docker-compose -f docker-compose.test.yml ps
        Name                 Command             State           Ports         
    ---------------------------------------------------------------------------
    csaf_backend   ./boot.sh                     Up      0.0.0.0:5000->5000/tcp
    csaf_db        docker-entrypoint.sh mongod   Up      27017/tcp
$ docker-compose -f docker-compose.test.yml down
```
### TODO: Remove
Build image:
```
$ cd csaf_backend/
$ docker build -f Dockerfile -t csaf_flask:0.0.1 .
```
Run database and backend containers:
```
$ docker run --name csaf_db -d \
    -p127.0.0.1:27017:27017 \
    --rm mongo:4.4.2
$ docker run --name csaf_backend -d \
    -p5000:5000 \
    --link csaf_db:dbserver \
    -e SECRET_KEY=CHANGE-ME \
    -e MONGODB_HOST=dbserver \
    --rm csaf_flask:0.0.1
$ docker container ls
```
### Development Setup
```
$ cd csaf_backend/
$ docker run --name csaf_db -d -p127.0.0.1:27017:27017 --rm \
    mongo:4.4.2
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install wheel IPython
$ pip install -r requirements.txt
$ flask run --host=127.0.0.1
```
### OIDC
Request an `access_token` with Keycloak:
```
curl -L -X POST 'http://<KEYCLOAK_IP>:8080/auth/realms/CSAF/protocol/openid-connect/token' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        --data-urlencode 'client_id=csaf-client' \
        --data-urlencode 'grant_type=password' \
        --data-urlencode 'client_secret=<CLIENT_SECRET>' \
        --data-urlencode 'scope=openid' \
        --data-urlencode 'username=<USER>' \
        --data-urlencode 'password=<PASSWORD>'
curl -L -X GET 'http://<CSAF_BACKEND_IP>:5000/api/advisories' -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

