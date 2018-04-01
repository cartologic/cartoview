FROM ubuntu:16.04
LABEL "MAINTAINER"="Cartologic Development Team"
ENV TERM xterm
RUN apt-get update
RUN apt-get install locales -y
RUN locale-gen "en_US.UTF-8" && update-locale
RUN apt-get install software-properties-common python-software-properties -y
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get update && apt-get install -y \
		gcc gettext \
                python-pip libpq-dev \
		sqlite3 git gdal-bin lsof psmisc \
                python-gdal python-psycopg2 \
                python-imaging python-lxml \
                python-dev libgdal-dev libgeoip-dev \
                python-ldap libxml2 libxml2-dev libxslt-dev \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python-pylibmc python-setuptools \
                curl build-essential build-essential python-dev \
	--no-install-recommends
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh -y
RUN apt-get install nodejs -y
RUN npm install -g bower grunt
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install --ignore-installed django-osgeo-importer geoip django-geonode-client \
                geonode==2.8rc11 django-jsonfield django-jsonfield-compat cartoview==1.5.9 \
                cherrypy==11.0.0 cheroot==5.8.3 django-haystack elasticsearch==2.4.0 \
		Whoosh --no-cache-dir
RUN rm -rf /var/lib/apt/lists/*
CMD ["/bin/bash"]
