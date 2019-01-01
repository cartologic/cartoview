FROM python:2.7-slim
LABEL "MAINTAINER"="Cartologic Development Team"
ENV PYTHONUNBUFFERED 1
ARG PROJ_DIR=/usr/local/pycartoview/code
ARG RUN_USER=cartoview
ARG RUN_GROUP=cartoview
ARG RUN_GID=2006
ARG RUN_UID=2002
ARG GEONODE_DEV=true
ARG GEONODE_SHA1=992daf724e83cdb0c1eb776d147eba841ad02cd9
# add our user and group first to make sure their IDs get assigned consistently, regardless of other deps added later
RUN groupadd -r -g ${RUN_GID} ${RUN_GROUP} \
	&& useradd -r -u ${RUN_UID} -g ${RUN_GROUP} ${RUN_USER}
RUN mkdir -p ${PROJ_DIR} \
	&& chown -R ${RUN_USER}:${RUN_GROUP} ${PROJ_DIR} && chmod g+s ${PROJ_DIR}
# include GDAL HEADER Files
# CPATH specifies a list of directories to be searched as if specified with -I,
# but after any paths given with -I options on the command line.
# This environment variable is used regardless of which language is being preprocessed.
ENV CPATH "$CPATH:/usr/include/gdal:/usr/include"
COPY scripts/docker/os_setup.sh ./
COPY scripts/docker/py_setup.sh ./
COPY scripts/docker/clean_up.sh ./
COPY scripts/docker/perm_setup.sh ./
COPY . /cartoview
RUN chmod +x *.sh
RUN ./os_setup.sh
RUN ./py_setup.sh
RUN ./clean_up.sh
RUN ./perm_setup.sh
VOLUME ${PROJ_DIR}
# switch to project dir
WORKDIR ${PROJ_DIR}
USER ${RUN_USER}
CMD ["/bin/bash"]
