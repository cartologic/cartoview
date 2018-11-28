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
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
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
# upgrade pip to latest version
RUN pip install --upgrade pip
RUN mkdir /code
COPY . /cartoview
WORKDIR /cartoview
# install cartoview
RUN pip install .
# switch to project dir
WORKDIR /code
# remove cartoview
RUN rm -rf /cartoview
# install additional packages and fix requirements(django-autocomplete-light==2.3.3)
RUN pip install --ignore-installed geoip django-geonode-client \
        django-autocomplete-light==2.3.3  --no-cache-dir
RUN apt autoremove --purge -y && apt autoclean -y
RUN rm -rf ~/.cache/pip
RUN rm -rf /var/lib/apt/lists/* && apt-get clean && \
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN echo "Yes, do as I say!" | apt-get remove --force-yes login	\
        && dpkg --remove --force-depends wget unzip 
CMD ["/bin/bash"]
