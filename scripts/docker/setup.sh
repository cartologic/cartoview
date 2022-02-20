#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
apt-get -y upgrade

# Install wget and gnupg
apt-get install wget gnupg -y

# Enable postgresql-client-13
echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
echo "deb http://deb.debian.org/debian/ stable main contrib non-free" | tee /etc/apt/sources.list.d/debian.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# To get GDAL 3.2.1 to fix this issue https://github.com/OSGeo/gdal/issues/1692
# TODO: The following line should be removed if base image upgraded to Bullseye
echo "deb http://deb.debian.org/debian/ bullseye main contrib non-free" | tee /etc/apt/sources.list.d/debian.list

# add gdal repo
#echo "deb http://http.us.debian.org/debian buster main non-free contrib" >>/etc/apt/sources.list
#add-apt-repository ppa:ubuntugis/ppa && apt-get update

# This section is borrowed from the official Django image but adds GDAL and others
apt-get update && apt-get install -y \
    libgdal-dev libpq-dev libxml2-dev \
    libxml2 libxslt1-dev zlib1g-dev libjpeg-dev \
    libmemcached-dev libldap2-dev libsasl2-dev libffi-dev

apt-get update && apt-get install -y \
    gcc zip gettext geoip-bin cron \
    postgresql-client-13 \
    sqlite3 spatialite-bin libsqlite3-mod-spatialite \
    python3-dev python3-gdal python3-psycopg2 python3-ldap \
    python3-pip python3-pil python3-lxml python3-pylibmc \
    uwsgi uwsgi-plugin-python3 \
    firefox-esr \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Prepraing dependencies
apt-get update && apt-get install -y devscripts build-essential debhelper pkg-kde-tools sharutils

# Install pip packages
pip install pip --upgrade \
    && pip install pygdal==$(gdal-config --version).* flower==0.9.4

# Activate "memcached"
apt install -y memcached
pip install pylibmc \
    && pip install sherlock

# install geonode from commit hash if dev enabled
#if [ "$GEONODE_DEV" = true ]; then
#       git clone https://github.com/GeoNode/geonode.git &&
#               cd ${APP_DIR}/geonode && pip install . &&
#               rm -rf /geonode
#fi

# create required dirs
mkdir -p ${APP_DIR}

# install cartoview [this will install GeoNode as a dependancy]
cd ${APP_DIR}/cartoview && pip install -e .  # && rm -rf /cartoview

# cleanup image
rm -rf ~/.cache/pip
rm -rf /root/.cache
apt autoremove --purge -y && apt autoclean -y && apt-get clean -y
rm -rf /var/lib/apt/lists/* && apt-get clean -y &&
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
echo "Yes, do as I say!" | apt-get remove --force-yes login &&
        dpkg --remove --force-depends wget
