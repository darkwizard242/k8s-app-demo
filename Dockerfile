FROM python:3.10-alpine

ARG APP_USER=${APP_USER:-tooling}
ARG APP_UUID=${APP_UUID:-1020}
ARG APP_GROUP=${APP_USER}
ARG APP_GUID=${APP_UUID}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && rm /code/requirements.txt

COPY ./app /code/app
RUN apk update \
    && apk upgrade --no-cache \
    && apk add --no-cache curl \
    && mkdir -pv /code/app \
    && addgroup -g ${APP_GUID} ${APP_GROUP} \
    && adduser -s /bin/sh -G ${APP_GROUP} -D -H -h /code/app -u ${APP_UUID} ${APP_USER} \
    && chown -R ${APP_USER}:${APP_GROUP} /code/app \
    && apk --purge del apk-tools

WORKDIR /code
USER ${APP_USER}
EXPOSE 80
HEALTHCHECK --start-period=10s --interval=15s --timeout=5s --retries=3 CMD curl -kv http://localhost/health/readiness || exit 1

CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "80"]
