# Cartoview 2
![Cartoview](https://img.shields.io/badge/Cartologic-Cartoview_2-blue.svg) ![Wagtail](https://img.shields.io/badge/Wagtail-CMS_2.x-green.svg)

![Start](https://img.shields.io/github/stars/cartologic/cartoview.svg?style=social) ![Forks](https://img.shields.io/github/forks/cartologic/cartoview.svg?style=social) ![Watchers](https://img.shields.io/github/watchers/cartologic/cartoview.svg?style=social)
## Quick Start
```
git clone -b cartoview2 --single-branch https://github.com/cartologic/cartoview.git
cd cartoview
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
> You must adjust the Database settings in settings > base.py - or create a local settings file
```python
python manage.py migrate
python manage.py loaddata initial_groups.json
python manage.py loaddata initial_users.json
python manage.py createcachetable
```
> run server
```python
python manage.py runserver
```

---
## Additonal Info
![Contrib](https://img.shields.io/github/contributors/cartologic/cartoview.svg)
![Languages](https://img.shields.io/github/languages/top/cartologic/cartoview.svg)
![License](https://img.shields.io/github/license/cartologic/cartoview.svg)