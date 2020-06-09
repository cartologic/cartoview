#!/usr/bin/env bash

apt-get update -y && apt-get install wget gnupg -y

# Enable postgresql-client-11.x
echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# This section is borrowed from the official Django image but adds GDAL and others
apt-get update && apt-get install -y \
		gcc \
		zip \
		gettext \
		postgresql-client-11 libpq-dev \
		sqlite3 \
		python3-gdal python3-psycopg2 \
		python3-pil python3-lxml \
		python3-dev libgdal-dev \
		libmemcached-dev libsasl2-dev zlib1g-dev \
		python3-pylibmc \
		uwsgi uwsgi-plugin-python3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

# install geoip-bin
printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
apt-get update && apt-get install -y geoip-bin

# Upgrade pip [Note from geonode-project template on github]
RUN pip install pip==20.1

# Install pygdal (after requirements for numpy 1.16 in GeoNode requirements.txt)
RUN pip install pygdal==$(gdal-config --version).*

# install geonode from commit hash if dev enabled
#if [ "$GEONODE_DEV" = true ]; then
#	git clone https://github.com/GeoNode/geonode.git &&
#		cd ${APP_DIR}/geonode && pip install . &&
#		rm -rf /geonode
#fi

# create required dirs
mkdir -p ${APP_DIR}

# install cartoview [this will install GeoNode as a dependancy]
cd ${APP_DIR}/cartoview && pip install -e .  # && rm -rf /cartoview

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
