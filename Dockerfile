FROM ubuntu:16.04
LABEL "MAINTAINER"="Cartologic Development Team"
ENV TERM xterm
RUN apt-get update
RUN apt-get install locales -y
RUN locale-gen ru_RU.UTF-8 && update-locale
RUN apt-get  install gdal-bin python-gdal -y
RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
                python-pip \
		libpq-dev \
		sqlite3 git \
                software-properties-common python-software-properties \
                lsof psmisc \
                python-gdal python-psycopg2 \
                python-imaging python-lxml \
                python-dev libgdal-dev \
                python-ldap \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python-pylibmc python-setuptools \
                curl build-essential build-essential python-dev \
	--no-install-recommends
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN apt-get upgrade -y
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh -y
RUN apt-get install nodejs -y
RUN npm install -g bower grunt
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install --ignore-installed GDAl django-osgeo-importer django-geonode-client \
                geonode==2.6.3 django-jsonfield django-jsonfield-compat cartoview \
                geonode-user-accounts==1.0.13 cherrypy==11.0.0 --no-cache-dir
RUN rm -rf /var/lib/apt/lists/*
CMD ["/bin/bash"]
