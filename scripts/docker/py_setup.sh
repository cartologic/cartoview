#!/usr/bin/env bash

# update python pip version
pip install --upgrade pip

# install python gdal stable
pip install GDAL==2.3.2

# install geonode from commit hash if dev enabled
if [ "$GEONODE_DEV" = true ]; then
	git clone https://github.com/GeoNode/geonode.git &&
		cd /geonode && git reset --hard ${GEONODE_SHA1} && pip install . &&
		rm -rf /geonode
fi
# create required dirs
mkdir -p ${PROJ_DIR}

# install cartoview
cd /cartoview && pip install . && rm -rf /cartoview
