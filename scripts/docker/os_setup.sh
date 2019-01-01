#!/usr/bin/env bash
apt-get update -y && apt-get install wget gnupg -y

# add postgres client latest
touch /etc/apt/sources.list.d/pgdg.list &&
	echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >>/etc/apt/sources.list.d/pgdg.list &&
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# add gdal repo
echo "deb http://http.us.debian.org/debian buster main non-free contrib" >>/etc/apt/sources.list

# geonode required libraries
apt-get update -y && apt-get install -y \
	build-essential gcc \
	git libxml2-dev libxslt-dev python-dev \
	gettext sqlite3 \
	python-lxml \
	postgresql-client libpq-dev python-psycopg2 \
	python-imaging \
	python-ldap \
	libmemcached-dev libsasl2-dev \
	python-pylibmc \
	gdal-bin libgdal-dev libgeos-dev \
	--no-install-recommends