FROM ubuntu:16.04
LABEL "MAINTAINER"="Cartologic Development Team"
ENV TERM xterm
RUN apt-get update
RUN apt-get install locales -y
RUN locale-gen en_US.UTF-8 && update-locale
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
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
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install --ignore-installed geoip django-geonode-client \
        geonode==2.8rc11 django-jsonfield django-jsonfield-compat \
        cartoview==1.8.2 cherrypy==11.0.0 cheroot==5.8.3 \
        django-autocomplete-light==2.3.3  --no-cache-dir
RUN pip install git+https://github.com/GeoNode/django-osgeo-importer.git
RUN rm -rf /var/lib/apt/lists/*
CMD ["/bin/bash"]
