# cartoview
Cartoview is a an app framework built with django on the top of [GeoNode](http://geonode.org/) , It extends Geonode with modules to install apps to better use the data, layers and maps provided from Geonode and Geoserver. 

### To install Cartoview :
  - For Windows , you can download GeoNode windows installer from [here](http://cartologic.com/cartoview/download/)
	
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
		
		# To start geoserver and django web server.
		paver start
		
	


    





