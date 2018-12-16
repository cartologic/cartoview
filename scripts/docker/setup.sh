#!/bin/bash

set -e

# geonode required libraries
apt-get update && apt-get install -y \
	build-essential gcc \
	git wget gnupg \
	gettext \
	sqlite3 libxml2-dev libxslt1-dev \
	python-imaging \
	python-dev python-ldap \
	libmemcached-dev libsasl2-dev zlib1g-dev \
	python-pylibmc \
	--no-install-recommends

# install stable postgres client
touch /etc/apt/sources.list.d/pgdg.list
echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >>/etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update && apt install postgresql-client libpq-dev python-psycopg2 -y

# update python pip version
pip install --upgrade pip

# add gdal debian repo
echo "deb http://http.us.debian.org/debian buster main non-free contrib" >>/etc/apt/sources.list
apt autoclean -y && apt autoremove -y && apt update -y
apt-get install -y gdal-bin libgdal-dev libgeos-dev

# install python gdal stable
pip install GDAL==2.3.2
if [ "$GEONODE_DEV" = true ]; then
	git clone https://github.com/GeoNode/geonode.git &&
		cd /geonode && git reset --hard ${GEONODE_SHA1} && pip install . &&
		rm -rf /geonode
fi
# create required dirs
mkdir -p ${APP_DIR}

# install cartoview
cd /cartoview && pip install . && rm -rf /cartoview

# cleanup image
apt autoremove --purge -y && apt autoclean -y
rm -rf ~/.cache/pip
rm -rf /var/lib/apt/lists/* && apt-get clean &&
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
echo "Yes, do as I say!" | apt-get remove --force-yes login &&
	dpkg --remove --force-depends wget unzip
