# csaf
Build the container image:
```
$ docker build -t csaf:latest .
$ docker images
```
Start containers:
```
$ docker run --name mongo -d -p27017:27017 mongo:latest
$ docker run --name csaf -d -p 5000:5000 --rm \
    -e SECRET_KEY=my-secret-key \
    --link mongo:dbserver \
    -e MONGODB_HOST=dbserver \
    csaf:latest
$ docker ps
```
```
$ docker container logs csaf
$ docker exec -it csaf sh
```


```
$ docker-compose up -d
$ docker-compose down
$ docker-compose down --volumes
```
