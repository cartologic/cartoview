# cartoview
Cartoview is an app framework built with django implemented as a [GeoNode](http://geonode.org/) project, It extends Geonode with modules to install web mapping apps to better use the data, layers and maps served from Geonode and Geoserver. 

### To install Cartoview :
  - For Windows , you can download cartoview windows installer from [here](http://cartologic.com/cartoview/download/)
	
  - For development:

		Prerequisites:
		# git		
		# Python 2.7		
		# Python setuptools 20.0
		# GDAL Core Libraries
		# Java JDK

		You have two options to set up the geos and gdal libraries. Either create an environment variable or uncomment the below lines at the top of your settings.py file .

		# os.environ['Path'] = r'C:/path/to/GDAL;' + os.environ['Path']
		# os.environ['GEOS_LIBRARY_PATH'] = r'C:/path/to/GDAL/geos_c.dll'
		# os.environ['GDAL_LIBRARY_PATH'] = r'C:/path/to/GDAL/gdal111.dll'
  
		git clone https://github.com/cartologic/cartoview.git
		cd cartoview.
		python setup.py install
		
		# To download geonode_geoserver and jetty.
		paver setup
		
		# Initialize database
		paver sync
		
		# To start geoserver and django web server.
		paver start
		
  - install bower dependencies
	```
	# install bower dependencies
	cd cartoview\cartoview
	bower install
	```
	
## For Ubuntu 14.04 development installation:

  1. Geonode Installation :
  
   - Required Packages Installation :
        ```sh
        $sudo apt-get install    \
        python-virtualenv      \
        build-essential        \
        openssh-server         \
        apache2                \
        gcc                    \
        gdal-bin               \
        gettext                \
        git-core               \
        libapache2-mod-wsgi    \
        libgeos-dev            \
        libjpeg-dev            \
        libpng-dev             \
        libpq-dev              \
        libproj-dev            \
        libxml2-dev            \
        libxslt-dev            \
        openjdk-7-jre          \
        patch                  \
        postgresql             \
        postgis                \
        postgresql-9.3-postgis-scripts \
        postgresql-contrib     \
        python                 \
        python-dev             \
        python-gdal            \
        python-pycurl          \
        python-imaging         \
        python-pastescript     \
        python-psycopg2        \
        python-support         \
        python-urlgrabber      \
        python-virtualenv      \
        tomcat7                \
        unzip                  \
        zip
        ```
	    
   - GeoNode Setup :
   
     - Let’s download GeoNode from the main GeoNode repository on GitHub:
        
        ```sh
        $git clone https://github.com/GeoNode/geonode.git --branch 2.5.x
        ```
     - create new user with home folder and move geonode to home folder of this user:
        
        ```sh
        $sudo useradd -m geonode
        $sudo mv ~/geonode /home/geonode/
        ```
      - now goto project folder using this command:
        
        ```sh
        $cd /home/geonode/geonode
        ```
      - install Geonode:
        
        ```sh
        $sudo pip install -e .
        ```
      - install Celery 3.1.25 to avoid some errors using:
        
            ```sh
            $sudo pip install celery==3.1.25
            ```
      - The following command will download a GeoServer web archive that we are going to use in GeoServer setup:

        ```sh
        $sudo paver setup
        ```
  2. Upgrade Python to latest version to avoid errors in cartoview :
   
   - python upgrade using the following commands:
        
        ```sh
        $sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
        $sudo apt-get update
        $sudo apt-get install python2.7
        ```
            
   - check python version using :
        
        ```sh
        $python --version
        ```
            
  3. Cartoview installion:
   - clone cartoview beside geonode folder :
   
        ```sh
        $sudo git clone https://github.com/cartologic/cartoview.git
        ```
   - goto cartoview folder using:
   
        ```sh
        $cd cartoview/
        ```
   - create apps folder:
   
        ```sh
        $sudo mkdir apps
        ```
   - install django-overextends package:
   
        ```sh
        $sudo pip install django-overextends
        ```
   - goto migrations folder of appmanager:
   
        ```sh
        $cd cartoview/appmanager/migrations
        ```
   - remove all files in migrations folder except  ```__init__.py``` from file explorer or using these commands:
   
        ```sh
        $sudo shopt -s extglob
        $sudo rm -- !(__init__.py)
        ```
   - back to cartoview project folder:
   
        ```sh
        $cd ../../../
        ```
   - run these commands :
   
        ```sh
        $sudo python manage.py makemigraions app_manager
        $sudo python manage.py migrate
        ```
   - run django server:
   
        ```sh
        $sudo python manage.py runserver
        ```
    now server is running on ```http://localhost:8000```

    
	




