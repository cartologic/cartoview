FROM python:3.7.6-stretch
LABEL "MAINTAINER"="Cartologic Development Team"

ENV PYTHONUNBUFFERED 1
ARG GEONODE_DEV=true
ARG APP_DIR=/usr/src/carto_app

# include GDAL HEADER Files
# CPATH specifies a list of directories to be searched as if specified with -I,
# but after any paths given with -I options on the command line.
# This environment variable is used regardless of which language is being preprocessed.
ENV CPATH "$CPATH:/usr/include/gdal:/usr/include"

COPY . ${APP_DIR}/cartoview
RUN chmod +x ${APP_DIR}/cartoview/scripts/docker/setup.sh
RUN ${APP_DIR}/cartoview/scripts/docker/setup.sh

# switch to project dir
VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}/cartoview

CMD ["/bin/bash"]
