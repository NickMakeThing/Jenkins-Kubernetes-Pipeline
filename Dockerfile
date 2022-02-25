FROM python:3.8-alpine

WORKDIR .

ARG BUILD_DEPS="build-base gcc libffi-dev"

ENV DJANGOKEY = fake-key
ENV BLOGPASSWORD = fake-password
ENV AWSACCESSKEYID = fake-key
ENV AWSSECRETACCESSKEY = fake-key

COPY requirements.txt .

RUN apk update \
        && apk add --nocache --virtual .build-deps ${BUILD_DEPS} \
        && apk add --no-cache postgresql-dev \
        && apk add jpeg-dev zlib-dev libjpeg \
        && pip3 install --upgrade pip \
        && pip3 install -r requirements.txt \
        && apk del .build-deps
COPY nicksblog .

CMD ["sh", "start.sh"]
