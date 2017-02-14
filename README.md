# Cartoview Installation
You Can Install Cartoview Using ```pip``` or ```easy_install``` open ```Terminal``` or Command ```Prompt``` and type :
- ```pip install -U cartoview```

or

- ```easy_install cartoview```

# Demo
- First step Follow instructions [here][1]

- configure Project Settings by renaming ```local_settings.py.sample``` in  ```project_name``` folder to ```local_settings.py```

- open ```local_settings.py``` and override Database paramters , also you can override any settings variable in this file.

- in your Project Folder open ```Terminal``` or ```Command Prompt```  type :

    ``` 
        python manage.py makemigrations app_manager
    	python manage.py migrate people
    	python manage.py migrate
    	python manage.py loaddata sample_admin.json
    	python manage.py loaddata json/default_oauth_apps.json
    	python manage.py runserver 0.0.0.0:8000 
    ```
- Now Demo is running on ```http://localhost:8000```

[1]: https://github.com/cartologic/cartoview-project-template
