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

# Enable postgresql-client-11.x
echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# add gdal repo
#echo "deb http://http.us.debian.org/debian buster main non-free contrib" >>/etc/apt/sources.list
#add-apt-repository ppa:ubuntugis/ppa && apt-get update

# This section is borrowed from the official Django image but adds GDAL and others
apt-get install -y \
                gcc \
                gettext \
                postgresql-client libpq-dev \
                sqlite3 \
                python3-psycopg2 \
                python3-lxml \
                python3-dev libgdal-dev \
                python3-ldap \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python3-pylibmc \
                libgeos-dev gdal-bin \
        --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Upgrade pip
pip install pip==20.1

# Update C env vars so compiler can find gdal
CPLUS_INCLUDE_PATH=/usr/include/gdal
C_INCLUDE_PATH=/usr/include/gdal

#let's install pygdal wheels compatible with the provided libgdal-dev
gdal-config --version | cut -c 1-5 | xargs -I % pip install 'pygdal>=%.0,<=%.999'

# install geoip-bin
printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
apt-get update && apt-get install -y geoip-bin

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
