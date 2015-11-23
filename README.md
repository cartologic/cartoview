# cartoview
Cartoview is a an app framework built with django on the top of [GeoNode](http://geonode.org/) , It extends Geonode with modules to install apps to better use the data ,layers and maps provided from Geonode and Geoserver. 

### To install Cartoview :
  1. Install GeoNode.
	- For Windows , you can download Geonde windows installer from [here](http://cartologic.com/cartoview/download/)
	- For Ubuntu , you can follow the [geonode official installation guide](http://docs.geonode.org/en/latest/tutorials/admin/install/quick_install.html#linux).
  2. After installing Geonode , Copy cartoview folder from the repository to **geonode project folder** - beside **geonode** folder and **manage.py** file.
  3. Copy **cartoview_settings.py**  to (geonode-project-folder/geonode) beside the main **settings.py**.
  4. Copy **base.html** from the repository to replace the one in (geonode-project-folder/geonode/templates).
  5. Copy **index.html** from the repository to replace the one in (geonode-project-folder/geonode/templates).
  6. Now edit the **(geonode-project-folder/geonode/settings.py)** file of Geonode and add this line at the end of the file:
  
  ```Python
  execfile (os.path.join(os.path.abspath(os.path.dirname(__file__)),"cartoview_settings.py"))
  ```
  7. Add cartoview urls to the **(geonode-project-folder/geonode/urls.py)** file , by adding these cde to the end of the file:
 
 ```Python
if "cartoview.app_manager" in settings.INSTALLED_APPS:
		urlpatterns += patterns('',
                        (r'^apps/', include('cartoview.app_manager.urls')),
                        )
 ```
  8. Add cartoview rest to Geonode , by registering it to geonode api through editing the file **(geonode-project-folder/geonode/api/urls.py)** and add these two lines to it :
  
  ```Python
  from cartoview.app_manager.rest import AppInstanceResource
  api.register(AppInstanceResource())
  ```
  9. Now run **collectstatic** and **syncdb** commands on the geonode project.
  10. Restart the server running the django project.
	- If Apache , run the commands:
	```Bash
	net stop apache-service-name
  net start apache-service-name
  ```


    





