![Cartoview Logo](img/cartoview-logo.png)
# For Developers

Cartoview provides [GeoApp Market](https://appstore.cartoview.net/) for GIS Developers.

## Create and Add your django app to Cartoview

***

Create a new empty app from **Cartoview App template** as below in your Cartoview project directory.

```shell
cd cartoview_project/apps
django-admin.py startapp --template=https://github.com/cartologic/Cartoview-app-template/archive/master.zip <app_name>
```

Edit ``cartoview_project/apps/apps.json`` and add an entry for your app. If you can't find `apps.json`, create it and add the following lines:

```json
{
    "app_name": {
        "active": true,
        "order": 1,
        "pending": false
    },
}
```

Add stores using the following command inside Cartoview project directory.

```shell
python manage.py loaddata app_stores.json
```

Add the new app to the database using the admin interface at `/admin`.

![Developers app](img/for-developers/developers_app.png)

!!! note
    Don't forget to check Single instance option if you want to test it for the first time.

![Developers app](img/for-developers/single_instance.PNG)
    
Now open Cartoview, navigate to ``Apps``, your app should be there.

![Developers app](img/for-developers/apps_panel.PNG)

Click ``Explore`` button to open the app home page.

![Developers app](img/for-developers/app_home.PNG)

Congratulations, now you have created your first app on Cartoview. You can upload it to [Cartoview App market](https://appstore.cartoview.net/) to make use of the features provided by this market.
