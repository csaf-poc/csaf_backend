FROM python:3.6.12-alpine3.12

LABEL MAINTAINER="Damian Pfammatter <damian.pfammatter@armasuisse.ch>"

ENV GROUP_ID=1000 USER_ID=1000

WORKDIR /var/www/

COPY ./requirements.txt /var/www/
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./app /var/www/app
COPY ./csaf.py ./config.py ./startup.sh ./oidc_client_secrets.json /var/www/
RUN chmod a+x startup.sh
RUN chmod a+w oidc_client_secrets.json

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000
ENTRYPOINT ["./startup.sh"]