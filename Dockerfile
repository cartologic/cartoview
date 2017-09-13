FROM ubuntu:16.04
MAINTAINER Cartologic Development Team
ENV TERM xterm
RUN apt-get update
RUN apt-get install locales -y
RUN locale-gen ru_RU.UTF-8 && update-locale
RUN apt-get -qq -y install wget curl git vim build-essential build-essential python-dev postgresql-client
RUN apt-get install software-properties-common python-software-properties -y
RUN apt-get install lsof -y
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get  install gdal-bin python-gdal -y
RUN apt-get install python-pip -y
RUN pip install GDAl --no-cache-dir
RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		libpq-dev \
		sqlite3 \
                python-gdal python-psycopg2 \
                python-imaging python-lxml \
                python-dev libgdal-dev \
                python-ldap \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python-pylibmc \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh -y
RUN apt-get install nodejs -y
RUN npm install -g bower
RUN npm install -g grunt
RUN mkdir /code
WORKDIR /code
RUN pip install cartoview -U --no-cache-dir
RUN pip install django-osgeo-importer --no-cache-dir
RUN pip install django-geonode-client --no-cache-dir
RUN pip install geonode -U --no-cache-dir
RUN pip uninstall Shapely -y
RUN pip install Shapely==1.5.17
RUN pip install django-jsonfield
RUN pip install django-jsonfield-compat
# better performance than uwsgi
RUN pip install cherrypy
CMD ["/bin/bash"]
