# csaf_backend
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
```
curl -L -X POST 'http://192.168.132.131:8080/auth/realms/CSAF/protocol/openid-connect/token' -H 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'client_id=csaf-client' --data-urlencode 'grant_type=password' --data-urlencode 'client_secret=<CLIENT_SECRET>' --data-urlencode 'scope=openid' --data-urlencode 'username=admin' --data-urlencode 'password=<PASSWORD>'
```
