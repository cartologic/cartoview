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

# update python pip version
pip install --upgrade pip

# install python gdal stable
pip install GDAL==2.4.0

# create required dirs
mkdir -p ${APP_DIR}

# install cartoview
git clone -b ${GIT_BRANCH} --recursive https://github.com/cartologic/cartoview.git &&
	cd /cartoview && pip install . && rm -rf /cartoview

django-admin.py startproject \
	--template=https://github.com/cartologic/Cartoview-project-template/archive/cartoview2.zip \
	--name wsgi.py,settings.py.local_settings.py cartoview_project ${APP_DIR}

# cleanup image
rm -rf ~/.cache/pip
rm -rf /root/.cache
apt-get purge --auto-remove -y gcc libgdal-dev libsasl2-dev \
	zlib1g-dev python-dev build-essential
apt autoremove --purge -y && apt autoclean -y && apt-get clean -y
rm -rf /var/lib/apt/lists/* && apt-get clean -y &&
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
echo "Yes, do as I say!" | apt-get remove --force-yes login &&
	dpkg --remove --force-depends wget
