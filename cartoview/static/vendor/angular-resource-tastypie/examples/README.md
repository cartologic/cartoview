#Instructions

```
IMPORTANT - USE PYTHON3
EX:
1. virtualenv env --no-site-packages --python=/usr/bin/python3
2. source env/bin/activate
```

##Backend:
1. cd backend/
2. pip install -r requirements.txt
3. cd myproject
4. ./manage.py makemigrations
5. ./manage.py migrate
6. ./manage.py runserver 0.0.0.0:8001

```
Django admin superuser "admin", password "abcd8585"
```

##Frontend:
1. cd frontend/
2. python3 -m http.server
```
Now, open your browser and go to 127.0.0.1:8000
```

```
IMPORTANT

If you downloaded the project with bower:

EX: "bower install angular-resource-tastypie"

Then install dependence for usability_app:
1. cd examples/frontend/usability_app
2. bower install bower.json
```
