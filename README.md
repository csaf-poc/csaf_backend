# csaf_backend
### Test Setup
The following steps can be used for testing the CSAF appserver. Note that the corresponding database is not persisted, and accesses performed by the DB root user.

Build appserver container image:
```
$ cd csaf_backend/
$ docker build -t csaf_flask:0.0.1 .
$ docker image ls
```
Start database and appserver containers:
```
$ docker run --name csaf_db -d -p27017:27017 --rm \
    mongo:4.4.2
$ docker run --name csaf_backend -d -p80:5000 --rm \
    --link csaf_db:dbserver \
    -e SECRET_KEY=CHANGE-ME \
    -e MONGODB_HOST=dbserver \
    csaf_flask:0.0.1
$ docker container ls
```
### Development Setup
```
$ cd csaf_backend/
$ docker run --name csaf_db -d -p27017:27017 --rm \
    mongo:4.4.2
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install wheel, IPython
$ pip install -r requirements.txt
$ flask run --host=127.0.0.1
```
