#Cartoview
##About Cartoview
Cartoview extends the popular GeoNode SDI to provide the ability to create, share, and visualize GIS Web Mapping Applications very easily and very quickly from the browser without programming.

Cartoview enables communities of users to share geospatial applications, to collaborate on these applications, and to exchange the underlying data as Open Geospatial Consortium (OGC) compliant web services

Cartoview has been built utilizing open source software and open standards to make it available for all GIS operators and to maximize interoperability.


##Key Features
[App Market][2] for GIS Web Application
Once you install GeoNode and CartoView you will be be able to install GIS applications directly from the browser

CartoView levereages the data management and security infrastructures of [GeoNode][1] to deploy and serve GIS applications

Developers create applications and deploy them on the [App Market][2]

Once the app is deployed it will become available to all Cartoview deployments



##Demos
You can take cartoview for a test [here][3]

Create your account, load some test data and start authoring web mapping applicaitons

##Frequently Asked Questions

- <h3>What exactly is CartoView? Is it a replacement for GeoNode?</h3>
	- CartoView is [Geo App market][2] for GeoNode. It is not a fork / improvement / reprlacement of Geonode, but rather additional code aimed at making it more extensible to integrate third party apps directly from the browser.

- <h3>What are the goals of Cartoview?</h3>
	- Sharing GIS Apps
	- Provide apps for common tasks like visualizing and querying feature services.
	- Extend the functions of the GeoNode SDI beyond data management
	- Provide a solid core of utilities that can be used to help developers integrate and deploy their Geo apps 
	- Foster an ecosystem of apps extending easily deplyable and installable
	
- <h3>Can I use CartoView with GeoNode Version 2.4 and earlier?</h3>
	- CartoView starts working with GeoNode 2.6

- <h3>I have an idea! What should I do?</h3>
	- Please file an issue. [Issues][5] are a great way to discuss new ideas, build consensus and talk about implementation details.

- <h3>I built something with cartoview can I show you?</h3>
	- Absolutely! Share it on twitter with [@ahmednosman][9] , [@cartoview][10]. You can add your project to the list in the readme too.

- <h3>I built a reusable app  can I contribute it?</h3>
	- Ofcourse. This is the purpose of Cartoview. Read the instructions on developing and deploying apps. Create an account on cartoview.org and load your app. Your app will be immediately available to all Cartoview deployments

- <h3>What are some good CartoView Apps?</h3>
	- [Simple Map Viewer][6] : This app allows the creation of html mobile ready viewer app with most basic features.
	- [Feature Detailed Viewer][7] : A map and list applications for store locations or similar usage
	- [WebApp Builder][8] : A customizable GIS 

- <h3>Running CartoView on GeoNode and QGIS Server?</h3>
	- There is no reason for Cartoview not to work on this deployment. (This was never tested). Apps relying on GeoServer ofcourse will not work

##Installation Requirements
- Install [Python2.7](https://www.python.org/)
- Install [1.8.7 <= Django <1.9a0](https://pypi.python.org/pypi/Django/1.8.7)



##Install On Ubuntu linux
- Follow these setps if you don't have Geonode  installed on your ubuntu system.<br/>

- These instructions will install [Geonode][1] and Cartoview.

	!!! note
	    Verify your installation is completed by adding any layer in [Geonode][1]

- Install [Geonode=2.5.15][1] 

- Install CartoView Libraries

	``` python
	pip install cartoview
	```


- Install CartoView_Django Project

	``` sh
	django-admin.py startproject --template=https://github.com/cartologic/cartoview-project-template/archive/master.zip <your_project_name>
	```

- Go to your Project Folder 

	``` sh
	cd <your_project_name>
	```


- Detect changes in ```app_manager``` App

	``` sh
	python manage.py makemigrations app_manager
	```

- create people Table

	``` sh
	python manage.py migrate people
	```

- Create Rest of tables :

	``` sh
	python manage.py migrate
	```

- load default User

	``` sh 
	python manage.py loaddata sample_admin.json
	```

- load default oauth app

	``` sh
	python manage.py loaddata json/default_oauth_apps.json
	```	

- Test Server (Development)
	- To start Development Server run this Command :

		``` sh
		python manage.py runserver 0.0.0.0:8000 
		```

!!! Note "Info"	
	 **(Optional)** if want to override any settings variable rename ```local_settings.py.sample``` to ```local_settings.py``` then override settings you want inside ```local_settings.py```

			
!!! warning
	Don't Forget to Change ```<your_project_name>``` to desired name.

!!! important "Apps From Geo App Market"	
	- to Install apps from [Geo App Market][2] 
		
	- Load Default Store

		``` sh
		python manage.py loaddata app_stores.json
		```
	
	- Now you Can Install Apps from [Geo App Market][2] 
	- Go to ```apps``` tab and click ```manage apps``` Button and install app you want
	
##Install On Windows

**We recommend to use Docker**

- Install [Make](http://gnuwin32.sourceforge.net/install.html)

- Follow [Docker Instructions](cartoview.md#docker)

##Existing GeoNode Users
Check GeoNode and Cartoview version compatibility in [PYPI][4] then install Cartoview

- Requirements:
	- GeoNode == 2.5.15

	!!! attention
		We will Support more version of Geonode Soon!!

- install cartoview libraries

	``` sh 
	pip install cartoview == <version>
	```

- Create Cartoview Project

	``` sh
	django-admin.py startproject --template=https://github.com/cartologic/cartoview-project-template/archive/master.zip <your_project_name>
	```

- Go to your Project Folder 

	``` sh
	cd <your_project_name>
	```

- detect Changes in app_manager

	``` sh
	python manage.py makemigrations app_manager
	```

- create People table 

	``` sh
	python manage.py migrate people
	```

	!!! bug
		this command will fire an error ignore it

- create rest of database tables 
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

##Docker
- be sure you installed all [requirements](cartoview.md#installation-requirements)
- Install [Docker][11]
- Create Cartoview Project which contains required files to run and configure Docker using this command:

	``` python
	django-admin.py startproject --template=https://github.com/cartologic/cartoview-project-template/archive/master.zip <your_project_name>
	```

- Replace ```<your_project_name>``` with desired name here i will use ```cartoview_project```

- Go to your project Folder 
	 ``` python
	 cd <your_project_name>
	 ```
- If you want to run this project on localhost only change two variables(project,module) in ```uwsgi.ini```(this is the server file) file in your Project Folder :
	```
	project = <your_project_name>
	.....
	module= <your_project_name>.wsgi:application
	```
- If you want to run this project with a domain :
	1. repeat previous step
	2. change ```django.env```(this is the file of the common django setting variables) file in your Project Folder to be some thing like this:

	!!! tip 
		default database username: ```cartologic``` and password:```root```


	``` python
	DATABASE_URL=postgres://<database_user_name>:<database_password>@postgis:5432/cartoview
	GEOSERVER_PUBLIC_LOCATION=http://<your_domain_or_ip>/geoserver/
	GEOSERVER_LOCATION=http://geoserver:8080/geoserver/
	SITEURL=http://<your_domain_or_ip>
	ALLOWED_HOSTS=['*']
	```

	!!! tip
		default database user in ```postgis.env``` file in your project if want to change it. 

- Start Docker images(cartoview,geoserver,postgres) type :
	
	``` sh
	make up
	```

- detect changes in ```app_manager``` App:

	``` sh
	make prepare_manager
	```

- create  people table : 

	``` sh
	make migrate_people
	```

	!!! bug
		this command will fire an error ignore it

- create rest of  tabels : 
	
	``` sh
	make sync
	```

	!!! success "Success"
		Now you can Access cartoview on ```http://localhost``` or ```http://<your_domain_or_ip>```
	!!! warning "Important"
		Final step Configure Geoserver before uploading layers from [here](http://docs.geonode.org/en/master/tutorials/admin/geoserver_geonode_security/#geoserver-security-backend)

##Issues
If something isn't working the way you expected, please take a look at [previous issues][5] that resolve common problems first.

Have you found a new bug? Want to request a new feature? We'd love to hear from you. Please let us know by submitting an issue.

##For Developers

- **Cartoview Provides a [GeoApp Market][2] for GIS Developers.**

- **Develope your own App**

	- Create a new empty app from cartoview app template as follow in your cartoview project directory
	``` python
	django-admin.py startproject --template=https://github.com/cartologic/cartoview-project-template/archive/master.zip <your_project_name>
	```

	- Edit cartoview_project/apps/apps.yml and add entry for your app
	``` yml		
	- name: <app_name>
	  active: true
	  order: 0
	```
	- Add the App to the database form django admin interface

		![New App](img/developers_app.png)
		
	- **Don't forget to check Single instace option if u want to test it for the first time**

		![Single Instance](img/single_instance.PNG)

	- Now on Cartoview in Apps tab your app will Appear Some thing like this

		![App Panel](img/apps_panel.PNG)
		
	- Click Explore Button will open App home page
		
		![App Home](img/app_home.PNG)
	
	- Make Changes to your App 
		
	- Now Zip your App and Upload it to [GeoApp Market][2]
	
	- Login on [GeoApp Market][2] and click ```MYAPPS``` tab
	
	- Click ```Submit New App``` Button and Fill Required Info
	
	- Now Users can install your app
	


##Contributing to CartoView

Please refer to each project's style guidelines and guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

- Fork the repo on GitHub
- Clone the project to your own machine
- Commit changes to your own branch
- Push your work back up to your fork
- Submit a Pull request so that we can review your changes


!!! note
	Be sure to merge the latest from "upstream" before making a pull request!
	
[1]: https://github.com/GeoNode/geonode
[2]: http://www.cartoview.org
[3]: http://demo.cartoview.org
[4]: https://pypi.python.org/pypi/cartoview
[5]: https://github.com/cartologic/cartoview/issues
[6]: http://cartoview.org/app/cartoview_map_viewer/
[7]: http://cartoview.org/app/cartoview_feature_list/
[8]: http://cartoview.org/app/cartoview_geonode_viewer/
[9]: https://twitter.com/ahmednosman
[10]: https://twitter.com/cartoview
[11]: https://www.docker.com/products/docker
