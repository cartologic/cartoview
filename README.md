# cartoview
Cartoview is a an app framework built with django implemented as a [GeoNode](http://geonode.org/) project, It extends Geonode with modules to install web mapping apps to better use the data, layers and maps served from Geonode and Geoserver. 

### To install Cartoview :
  - For Windows , you can download cartoview windows installer from [here](http://cartologic.com/cartoview/download/)
	
  - For development::

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
		


## For Ubunu 14.04 development installation:

   Install geonode using [this instructions](http://docs.geonode.org/en/master/tutorials/install_and_admin/geonode_install/install_geonode_application.html)
   
		
		# Verify that Geonode installation is working by the following commands:
		cd <geonode_folder>
		python manage.py validate 
		
		# To install Cartoview follow these commands:
		git clone https://github.com/cartologic/cartoview.git

		#Tthere is no specific path to clone Cartoview

		cd <cartoview_folder>
		
		# To download geonode_geoserver and jetty.
		paver setup
		
		# Initialize database
		paver sync
		
		# To start geoserver and django web server.
		python start


    
	




