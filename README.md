# csaf
### Test Setup
The following steps can be used for testing the CSAF appserver. Note that the corresponding database is not persisted, and accesses performed by the DB root user.

Build appserver container image:
```
$ cd csaf/
$ docker build -t csaf_api:0.0.1 .
$ docker image ls
```
Start database and appserver containers:
```
$ docker run --name csaf_dbserver -d -p27017:27017 --rm \
    mongo:4.2.2
$ docker run --name csaf_appserver -d -p5000:5000 --rm \
    --link csaf_dbserver:dbserver \
    -e SECRET_KEY=CHANGE-ME \
    -e MONGODB_HOST=dbserver \
    csaf_api:0.0.1
$ docker container ls
```
