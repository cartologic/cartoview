#CartoView

## This document describes the Installation of CartoView on Ubuntu with GeoNode 2.6.3
    
!!! warning
	In case of any other version of GeoNode before 2.5 these steps will not be applicable.

##Installation Requirements
- Install [Python2.7](https://www.python.org/download/releases/2.7/).

- Install Django
```
sudo apt-get update
sudo apt-get install python-django

```

!!! note
    For more information about Djano installation visit [1.8.7 <= Django <1.9a0](https://pypi.python.org/pypi/Django/1.8.7).


##Install Required Packages on ubuntu linux

- Run the following command  


		 sudo apt-get update
		 sudo apt-get install python-virtualenv python-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libpq-dev libgdal-dev git default-jdk


## Database Installation
- Install PostgreSQL Database
	```
	sudo apt-get install postgresql postgresql-contrib
	```


- Install PostGIS ( Extension to support Geographic objects that allows location queries to be run in SQL. )

	```
	sudo apt-get install postgis
	```



		sudo apt-get install pgadmin3
!!! note
	    you can install pgAdmin ( PostgreSQL GUI tool using ): ``` sudo apt-get install pgadmin3```

!!! note
		For more Information about PostgreSQL visit [postgresql](https://www.postgresql.org/download/linux/ubuntu/).

## Database Configuration

 - You will need to log in with a user called postgres created by the installation to manage the database
 ```
 sudo -i -u postgres
 ```
 - Change the postgres user password
 ```
 psql
 \password
 ```
 - Exit the PostgreSQL prompt by typing
 ```
 \q
 ```
 - Create two new databases cartoView and cartoview_datastore
 ```
 createdb cartoview
 createdb cartoview_datastore
 ```

!!! note
     You can change the databases' name but make sure to change thier names in the local_settings.py file in cartoview project directory
 - Add PostGIS extension to the created databases

 ```
 psql <database-name>
 CREATE EXTENSION postgis;
 ```

!!! note
    For more information about PostgreSQL configuration visit [postgreSQL](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

##Install GeoServer

- Install Java 8 (needed by GeoServer)
```
sudo apt-add-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

1) Download  [Tomcat v9]( https://tomcat.apache.org/download-90.cgi)

2) Extract the tar folder and rename it tomcat

3) Download GeoServer war file from [here](http://build.geonode.org/geoserver/latest/geoserver-2.9.x-oauth2.war)

4) Rename the war file to geoserver.war

5) Copy the war file inside webapps directory in tomcat

6) Create tomcat user by editing the tomcat-users.xml file:


			sudo nano path/to/tomcat/conf/tomcat-users.xml

!!! note
    Make sure to change path/to/tomcat in the previous command with your tomcat path


7) Paste the following line in tomcat-users.xml
```<user username="admin" password="password"roles="manager-gui,admin-gui"/>
```
just before ```</tomcat-users > ``` and change the username and password

8) Edit context files in host-manager directory

     sudo nano path/to/tomcat/webapps/host-manager/META-INF/context.xml

9) Comment the line ``` <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> ``` by changing it to
				 ```
				 <!--<Valve className="org.apache.catalina.valves.RemoteAddrValve"
								 allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
				 ```

10) Edit context files in manager directory

    sudo nano path/to/tomcat/webapps/manager/META-INF/context.xml

11) Comment the line ``` <Valve className="org.apache.catalina.valves.RemoteAddrValve"
        allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> ```  by changing it to
				```
				<!--<Valve className="org.apache.catalina.valves.RemoteAddrValve"
								allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
				```  

- Start tomcat server

   ``` sh path/to/your/tomcat/bin/startup.sh
	 ```

- !!! note
      For more information about tomcat Installation and Configuration of tomcat visit [tomcat](https://www.digitalocean.com/community/tutorials/how-to-install-apache-tomcat-8-on-ubuntu-16-04)
- !!! warning "Important"
    Cartview must be up and running

- !!! warning "Important"
	In Production Configure GeoServer before uploading layers from [here](http://docs.geonode.org/en/master/tutorials/admin/geoserver_geonode_security/#geoserver-security-backend)

## GeoNode 2.6.3 Installation
 - Follow these setps if you don't have Geonode installed on your ubuntu system.<br/>

 - Create and activate the python virtual environment

		virtualenv <your_virtual_env_name>
		source <your_virtual_env_name>/bin/activate

 - Install pip ( a package management system used install and manage software packages written in Python )

		sudo apt-get install python-pip


 - Install geonode 2.6.3


		pip install geonode==2.6.3
		sudo apt-get install python-gdal


 - Create a symbolic link of OSGeo in your virtualenv needed by GDAL to run properly  


		ln -s /usr/lib/python2.7/dist-packages/osgeo  <your_virtual_env_name>/lib/python2.7/site-packages/osgeo   



!!! note
	    To Verify installation add any layer in [Geonode][1]



##  CartoView Libraries Installation

- Install CartoView

	```
	pip install cartoview
	```


- Install CartoView_Django Project


        django-admin.py startproject template=https://github.com/cartologic/cartoview-project-template/archive/master.zip --name django.env,uwsgi.ini,.bowerrc,server.py <your_project_name>
       
	

- Go to your Project Folder
	
	       cd <your_project_name>
	


- Detect changes in ```app_manager``` App

	
	       python manage.py makemigrations app_manager
	

- Create account Table

	
	       python manage.py migrate account
	



- Create Rest of tables :


            python manage.py migrate


- Load default User

	
            python manage.py loaddata sample_admin.json


- Load default oauth app

	
	       python manage.py loaddata json/default_oauth_apps.json
	

- Test Development Server
by running this Command :

	
		      python manage.py runserver 0.0.0.0:8000
		

!!! Note "Info"
	 **(Optional)** if you want to override any  variable settings (for example to change the
	  database password ,name or hostname ) rename``` local_settings.py.sample``` to ```local_settings.py``` then override settings you want inside ```local_settings.py```


!!! warning
	Don't Forget to Change ```<your_project_name>``` to desired name.

!!! important "Apps From GeoApp Market"
	- To Install apps from [GeoApp Market](http://www.cartoview.org)

	- Load Default Store

		```
		python manage.py loaddata app_stores.json
		```

  	- Install [nodejs](https://nodejs.org/en/) and then install [bower](https://bower.io/) we need them to install app_manager dependencies
	- In this step we will install required files in your project folder type :
		```
		bower install
		```
	- Collect Required files type:
		```

		python manage.py collectstatic --noinput
		```
	- Now you Can Install Apps from [Geo App Market][2]
	- Go to ```apps``` tab and click ```manage apps``` Button and install app you want





##Deployment Notes

- !!! warning "Important"
	In Production Configure GeoServer before uploading layers from [here](http://docs.geonode.org/en/master/tutorials/admin/geoserver_geonode_security/#geoserver-security-backend)

- !!! warning "Important"
	Once CartoView is installed it is expected to install all apps from the App Store automatically
	At the moment CartoView will fully support Apache server only
	For nginx deployments, CartoView will be able to detect new apps and get the updates, how ever to apply the updates, web server restart will be required to complete 	the process
	CartoView will not be able to restart nginx when new apps are installed.
	After you install or update apps from the app manager page you will need to restart nginx manually until this issue is addressed in the future
	- Follow these steps to get apps working on nginx
		- Collect static files using this commands
			```
			python manage.py collectstatic --noinput
			```
		- Restart server now you should restart server after installing any app

