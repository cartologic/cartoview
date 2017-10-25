#Cartoview

##For Developers

- CartoView Provides  [GeoApp Market](http://www.cartoview.org) for GIS Developers.

- Develope your own App

	- Create a new empty App from CartoView App template as follow in your cartoview project directory 
	``` python
	cd apps
	django-admin.py startapp --template=https://github.com/cartologic/cartoview-app-template/archive/master.zip <your_App_name>
	```

	- Edit cartoview_project/apps/apps.yml and add entry for your app or create apps.yml file ,If ou cannot find it ,Add the following lines:
	``` yml
	- name: <app_name>
	  active: true
	  order: 0
	```
	- Add stores using the following command inside CartoView project directory
	```
	python manage.py loaddata app_stores.json

	```
    
	- Add the new App to the database form Django admin interface

		![New App](img/developers_app.png)

	- Don't forget to check Single instance option if u want to test it for the first time

   ![New App](img/single_instance.PNG)

- Now on CartoView Apps tab your app will Appear like this

![App Panel](img/apps_panel.PNG)

- Click Explore Button to open App home page

![App Home](img/app_home.PNG)

!!! success
    Congratulations, now you have created your first App on CartoView
    you can upload it to cartoview App market to make use of the features
    provided by cartoview App market


