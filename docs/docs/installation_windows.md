#Cartoview

### This document describes the Installation of CartoView with GeoNode on Windows 2.6.3

!!! warning
	In case of any other version of GeoNode before 2.5 these steps will not be applicable.

##Installation Requirements

- Install [Python2.7](https://www.python.org/download/releases/2.7/)
	- Make Sure to add Python to the Path, as this is not done by default 
    
	- Add python.exe to the PATH
    <br/> <br/>
		![python setup](img/python.png)
        ![python setup](img/python2.png)
        
		<br/>
        
- Install Django 1.8.7 
     , Open Command Prompt then type:

	```sh
	pip install django==1.8.7
	```


##Existing GeoNode Users
Check GeoNode and CartoView version compatibility in [PYPI](https://pypi.python.org/pypi/cartoview) Then install CartoView

## Requirements:

 GeoNode == 2.6.3


- Install CartoView Libraries

	``` sh
	pip install cartoview == <version>
	```

- Create CartoView Project

	``` sh
	django-admin.py startproject --template=https://github.com/cartologic/cartoview-project-template/archive/master.zip --name django.env,uwsgi.ini,.bowerrc <your_project_name>
	```

- Go to your Project Folder

	``` sh
	cd <your_project_name>
	```

- Detect Changes in app_manager

	``` sh
	python manage.py makemigrations app_manager
	```

- Create account table

	``` sh
	python manage.py migrate account
	```



- Create rest of database tables
	``` sh
	python manage.py migrate
	```

- Collect static Files

	``` sh
	python manage.py collectstatic --noinput
	```

- Now Development Server :
	``` sh
	python manage.py runserver 0.0.0.0:8000
	```
##Deployment Notes

- !!! warning "Important"
	In Production Configure GeoServer before uploading layers from [Here](http://docs.geonode.org/en/master/tutorials/users/managing_layers/upload.html)

- !!! notes "Notes"
    - Once CartoView is installed it is expected to install all apps from the App store automatically
	- At the moment CartoView will fully support Apache server only
	For nginx deployments, CartoView will be able to detect new apps and get the updates, How ever to apply the updates, web server restart will be required to complete the process.
	- CartoView will not be able to restart nginx when new apps are installed.
	- After you install or update apps from the app manager page you will need to restart nginx manually until this issue is addressed in the future
	- Follow these steps to get apps working on nginx
		- Collect static files using this commands
			``` sh
			python manage.py collectstatic --noinput
			```
		- Restart server now you should restart server after installing any app

