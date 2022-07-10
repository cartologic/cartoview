FROM python:3.10.2-buster
LABEL "MAINTAINER"="Cartologic Development Team"

ENV PYTHONUNBUFFERED 1
ARG GEONODE_DEV=true
ARG APP_DIR=/usr/src/carto_app

COPY . ${APP_DIR}/cartoview
RUN chmod +x ${APP_DIR}/cartoview/scripts/docker/setup.sh
RUN ${APP_DIR}/cartoview/scripts/docker/setup.sh

VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}/cartoview

CMD ["/bin/bash"]
