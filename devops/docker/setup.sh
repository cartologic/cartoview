#!/usr/bin/env bash

apt-get update -y && apt-get install wget gnupg -y

# add postgres client latest
touch /etc/apt/sources.list.d/pgdg.list &&
	echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >>/etc/apt/sources.list.d/pgdg.list &&
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# add gdal repo
echo "deb http://http.us.debian.org/debian buster main non-free contrib" >>/etc/apt/sources.list

# install required libs
apt-get update -y && apt-get install -y \
	build-essential gcc git \
	python-dev \
	gettext sqlite3 \
	postgresql-client libpq-dev python-psycopg2 \
	python-pil \
	python-ldap \
	libmemcached-dev libsasl2-dev \
	python-pylibmc \
	gdal-bin libgdal-dev libgeos-dev \
	--no-install-recommends

# install npm
apt-get install -y npm

# update python pip version
pip install --upgrade pip

# install python gdal stable
apt-get install -y libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip install GDAL==2.4.0

# create required dirs
mkdir -p ${APP_DIR}

# update files
apt-get update
apt-get install -y build-essential gcc

#adjust pip
pip install pip==9.0.1

#adjust setup tools
pip install setuptools==45

# install cartoview
git clone -b ${GIT_BRANCH} --recursive https://github.com/cartologic/cartoview.git &&
	cd /cartoview && pip install . && rm -rf /cartoview
