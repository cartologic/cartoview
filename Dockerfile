FROM python:2.7-slim
LABEL "MAINTAINER"="Cartologic Development Team"
ENV PYTHONUNBUFFERED 1
ARG GEONODE_DEV=true
ARG GEONODE_SHA1=992daf724e83cdb0c1eb776d147eba841ad02cd9
ARG APP_DIR=/usr/src/carto_app
# include GDAL HEADER Files
# CPATH specifies a list of directories to be searched as if specified with -I,
# but after any paths given with -I options on the command line.
# This environment variable is used regardless of which language is being preprocessed.
ENV CPATH "$CPATH:/usr/include/gdal:/usr/include"
COPY scripts/docker/setup.sh ./
COPY . /cartoview
RUN chmod +x setup.sh
RUN ./setup.sh
# switch to project dir
VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}
CMD ["/bin/bash"]
