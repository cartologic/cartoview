![Cartoview Logo](../img/cartoview-logo.png)
# Cartoview Installation | Ubuntu

## Introduction
This document describes the installation of Cartoview with GeoNode 2.10.3 on Ubuntu 18.04.

## Installation Requirements
- **Install Python2.7 and Django**
```shell
sudo apt-get update
sudo apt-get install python-pip python-django
```

!!! note
    This will install the latest compatible with Python2.7 version of django which is 1.11.11 for now.

- **Install the following required packages**
```shell
sudo apt-get update
sudo apt-get install python-virtualenv python-dev python-gdal libxml2 libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libpq-dev libgdal-dev git default-jdk
```
Verify that the important packages are installed successfully. (The versions should be something like what after #)
```shell
python --version      
# Python 2.7.17

django-admin --version
# 1.11.11

virtualenv --version
# 15.1.0

update-java-alternatives –l 
# java-1.11.0-openjdk-amd64 1111 /usr/lib/jvm/java-1.11.0-openjdk-amd64

python -c "from osgeo import gdal; print gdal.__version__"
# 2.2.3
```

## Database Installation
- **Install PostgreSQL Database**

```shell
sudo apt-get install postgresql postgresql-contrib
```

- **Install PostGIS**

It's a spatial database extender for [PostgreSQL][1] database. It adds support for geographic objects allowing location queries to be run in SQL.

[1]: https://www.postgresql.org/

```shell
sudo apt-get install postgis
```

!!! note
    Optional | You can also install [pgAdmin][2] ( A PostgreSQL GUI tool using ): `sudo apt-get install pgadmin4`
!!! note
    For more Information, visit [PostgreSQL dowload page][3].
    
[2]: https://www.pgadmin.org/
[3]: https://www.postgresql.org/download/linux/ubuntu/

## Database Configuration
- **Configure PostgreSQL interactive terminal to create the databases**

You will need to log in with a user called postgres created by the installation to manage the database.

```shell
sudo -i -u postgres
```
Change the postgres user password.
```shell
psql
```
This will open PostgreSQL interactive terminal and you can set the postgres user password by typing:
```shell
\password
```
Exit the PostgreSQL prompt by typing:
```shell
\q
```

- **Create two new databases** ``cartoview`` **and** ``cartoview_datastore``

```shell
createdb cartoview
createdb cartoview_datastore
```

!!! note
    You can change the name of the databases but make sure to change their names also in the ``local_settings.py`` file in Cartoview directory after you have installed it as the file is pre-configured for these names specifically.
    
- **Add PostGIS extension to the created databases to deal with the geographic objects**

For ``cartoview`` database: (Copy the command before the hash symbol)

```shell
psql cartoview               # To be executed at ubuntu terminal
CREATE EXTENSION postgis;    # To be executed at psql terminal
```

Exit the PostgreSQL terminal with ``\q``

For ``cartoview_datastore`` database: (Copy the command before the hash symbol)

```shell
psql cartoview_datastore    # To be executed at ubuntu terminal
CREATE EXTENSION postgis;   # To be executed at psql terminal
```

!!! note
    The previous step must be done for the two databases, ``cartoview`` and ``cartoview_datastore``.

You can now logout back to your usual user (other than postgres) by just typing ``exit``.

## GeoNode 2.10.3 Installation

Follow these setps if you don't have GeoNode 2.10.3 installed.

- **Create a Python Virtual Environment**

Let's make a directory called ``cartoview_service`` (You can name it whatever you prefer) that will contain two folders, python virtual environment and cartoview.

```shell
mkdir cartoview_service
cd cartoview_service
```

Create and activate the python virtual environment, we will name it ``cartoview_venv``.

!!! note
    You can name it whatever you prefer, but bare in mind to change every ``cartoview_venv`` in the commands below with the name you want for your virtual environment.
    
```shell
virtualenv cartoview_venv
source cartoview_venv/bin/activate
```

!!! note
    - You would notice how your prompt is now prefixed with the name of the virtual environment, ``cartoview_venv`` in our case.
    
    - Make sure you have installed ``python-pip`` and ``python-gdal`` as we have done above. We will use them to install and run GeoNode and Cartoview.
    
    - From now on, each command associated with geonode or cartoview must be executed while the virtual environment is activated.
    
- **Install geonode 2.10.3**

```shell
pip install geonode==2.10.3
```

## Cartoview Libraries Installation

!!! warning
    Make sure you're inside ``cartoview_service`` directory and the ``cartoview_venv`` is still activated.

- **Download and install Cartoview**

Download the latest version of cartoview by cloning the repository.

```shell
git clone https://github.com/cartologic/cartoview.git
```

This will create a folder called ``cartoview`` inside ``cartoview_service`` directory.

Now we need to install cartoview dependencies, but first go to ``cartoview`` directory.

```shell
cd cartoview
pip install -e .
```

!!! warning
    Make sure you got the dot ``.`` when you copy the previous command.
    
- **Make sure the created databases are in the ``settings.py`` file**

Go to ``cartoview`` directory, you will find inside it another folder called ``cartoview``. Navigate inside it also.

You should find a file called ``local_settings.py.sample``. Remove the last word ``sample``.

```shell
cp local_settings.py.sample local_settings.py
```

This will override the ``settings.py`` file with a another configured settings file which is ``local_settings.py``.

If you print the contents of ``local_settings.py`` with the below command.

```shell
cat local_settings.py
```

You can see the databases that we have created above inside ``local_settings.py`` as below.

```
DATABASES = {
  'default': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis',
      'NAME': 'cartoview',
      'USER': 'postgres',
      'PASSWORD': 'cartoview',
      'HOST': 'localhost',
      'PORT': '5432',
  },
  # vector datastore for uploads
  'datastore': {
      'ENGINE': 'django.contrib.gis.db.backends.postgis’,
      'NAME': 'cartoview_datastore',
      'USER': 'postgres',
      'PASSWORD': 'cartoview',
      'HOST': 'localhost',
      'PORT': '5432',
  }
}
```

!!! note
    If you want to override any variable settings (for example to change the database password ,name or host), you can do this inside ``local_settings.py`` to override the settings in ``settings.py``.
    
- **Create a symbolic link of OSGeo in your virtualenv needed by GDAL to run properly**

```shell
ln -s /usr/lib/python2.7/dist-packages/osgeo  cartoview_venv/lib/python2.7/site-packages/osgeo
```

!!! note
    The point of creating a symbolic link is to share the development source code of GDAL (which is installed previously at [Installation Requirements][4] section) instead of copying it every time we need to use it inside a python virtual environment.
 
 [4]: #installation-requirements
 
- **Migrate & Load default data**

Inside ``cartoview`` folder, run the below commands to migrate and load Cartoview data.

!!! note
    Make sure the virtual environment is still activated (If you see its name prefixed your prompt, you're good to go).

Detect changes in the ``app_manager``.
```shell
python manage.py makemigrations app_manager
```

Migrate the data.
```shell
python manage.py makemigrations
python manage.py migrate
```

Create accounts table.
```shell
python manage.py migrate account
```

Load default User.
```shell
python manage.py loaddata sample_admin.json
```

Load default oauth apps so that you will be able to authenticate with defined external server.
```shell
python manage.py loaddata default_oauth_apps.json
```

Load default Initial Data for Cartoivew.
```shell
python manage.py loaddata initial_data.json
```

Load default Cartoview Appstore data.
```shell
python manage.py loaddata app_stores.json
```

- **Test Development Server by running this Command**
```shell
python manage.py runserver 0.0.0.0:8000
```

At ``localhost:8000``, you should get:

![Cartoview website](../img/installation/Ubuntu/cartoview.png "Cartoview")

**Sign-in with:**
```shell
user: admin
password: admin
```

Now we have Cartoview up and running, last thing we need to do, is to install and configure GeoServer to run with it.

## GeoServer 2.16.2 Installation 
We need to install Tomcat to be able to run GeoServer inside it as a Java application.

- **Install and configure Tomcat 9**

!!! warning
    Make sure you have installed ``default-jdk`` as we have done before.
    
We will create a new group and a user that will run and control the tomcat service.

```shell
sudo groupadd tomcat
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
```

!!! note
    We made this user a member of the tomcat group, with a home directory of ``/opt/tomcat`` (where we will install Tomcat), and with a shell of ``/bin/false`` (so nobody can log into the account).
    
Now we will download Tomcat 9, Navigate to ``/tmp`` directory (we will download Tomcat there, you can download it anywhere else).

```shell
cd /tmp
curl -O https://downloads.apache.org/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz
```

Tomcat used to be installed in the directory ``/opt/tomcat``. So we will extract and install it there too.

```shell
sudo mkdir /opt/tomcat
sudo tar xzvf apache-tomcat-9.0.33.tar.gz -C /opt/tomcat --strip-components=1
```

Now we should set up the tomcat user that we have created before to have the permissions of the directory ``/opt/tomcat``.

```shell
cd /opt/tomcat
sudo chgrp -R tomcat /opt/tomcat
sudo chmod -R g+r conf
sudo chmod g+x conf
sudo chown -R tomcat webapps/ work/ temp/ logs/
```

!!! note
    Basically, what we have done in the previous step:

    - Give the tomcat group the ownership over the entire installation directory.
    - Give the tomcat group read access to the ``conf`` directory and all of its contents, and execute access to the directory itself.
    - Make the tomcat user to be the owner of the webapps, work, temp, and logs directories.
    
**Let’s create a system service to manage tomcat startup.**
```shell
sudo nano /etc/systemd/system/tomcat.service
```

Copy the text below inside this file.
```shell
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
Environment=CATALINA_PID=/opt/tomcat/temp/tomcat.pid
Environment=CATALINA_HOME=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=tomcat
Group=tomcat
UMask=0007
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```

!!! warning
    For ``Environment=JAVA_HOME``, make sure you have added the correct path for you installed version of Java.

**To test the service:**
```shell
sudo systemctl daemon-reload
sudo systemctl start tomcat.service
sudo systemctl status tomcat.service
```
To make the service enabled by default permanently.
```shell
sudo systemctl enable tomcat.service
```

**Configure Tomcat Web Management Interface**

In order to use the manager web app that comes with Tomcat, we need to add a login user to our Tomcat server. We will do this by editing ``tomcat-users.xml`` file.
```shell
sudo nano /opt/tomcat/conf/tomcat-users.xml
```
Add the following line to be between ``tomcat-users`` tags. You can set the username and password that you prefer. For us, username will be ``admin`` and password to be ``cartoview``.
```shell
<user username="admin" password="cartoview" roles="manager-gui,admin-gui"/>
```
By default, newer versions of Tomcat restrict access to the Manager and Host Manager apps to connections coming from the server itself. You might want to alter this behaviour.

##### FOR MANAGER APP TYPE:
```shell
sudo nano /opt/tomcat/webapps/manager/META-INF/context.xml
```

##### FOR HOST MANAGER APP TYPE:
```shell
sudo nano /opt/tomcat/webapps/host-manager/META-INF/context.xml
```

Inside both, comment out the IP address restriction to allow connections from anywhere.

###### INSTEAD OF THIS:
```shell
<Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />
```

###### TO BE THIS:
```shell
<!--<Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
```

**Restart Tomcat service**
```shell
sudo systemctl restart tomcat.service
```

In the browser if you navigate to ``localhost:8080``, you should see Tomcat up and running and you can access the Manager App by logging in with the credentials you have entered inside ``tomcat-users.xml``.

**Download and Install GeoServer war file**

Now we will download the latest stable version of GeoServer war file from [here][5] or you can execute the following command.

[5]: https://build.geo-solutions.it/geonode/geoserver/latest/geoserver-2.16.2.war

```shell
cd /tmp
wget --no-check-certificate https://build.geo-solutions.it/geonode/geoserver/latest/geoserver-2.16.2.war
```

!!! note
    We have downloaded the war file inside ``/tmp`` directory, but you can download it anywhere else.
    
For simplicity, rename the file to be ``geoserver.war`` instead of ``geoserver-2.16.2.war``.
```shell
mv geoserver-2.16.2.war geoserver.war
```

Copy the ``geoserver.war`` file to ``/tomcat/webapps`` directory.
```shell
sudo cp geoserver.war /opt/tomcat/webapps/
```

Restart Tomcat so that it will be able to manage GeoServer as a web app.
```shell
sudo systemctl restart tomcat.service
```

This will cause Tomcat to serve GeoServer from the war file which we have put inside ``tomcat/webapps``.

!!! note
    Make sure that GeoServer is running:
    
    - Navigate to ``localhost:8080`` to open Tomcat then click on Manager App.
    
    - Login with the credentials, you have entered in ``tomcat-users.xml``.
    
    - You should find GeoServer under Applications section started already.

![Tomcat Application Manager](../img/installation/Ubuntu/tomcat_manager.png "Tomcat Application Manager")
    
Now GeoServer is up and running at ``localhost:8080/geoserver``.

![GeoServer](../img/installation/Ubuntu/geoserver.png "GeoServer")
**Sign-in with:**
```shell
user: admin
password: geoserver
```