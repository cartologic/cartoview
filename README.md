# Cartoview 2
![Cartoview](https://img.shields.io/badge/Cartoview-2-blue.svg) ![Wagtail](https://img.shields.io/badge/Wagtail_CMS-2.x-green.svg) ![Wagtail](https://img.shields.io/badge/Bootstrap-4-red.svg)

![Start](https://img.shields.io/github/stars/cartologic/cartoview_2.svg?style=social) ![Forks](https://img.shields.io/github/forks/cartologic/cartoview_2.svg?style=social) ![Watchers](https://img.shields.io/github/watchers/cartologic/cartoview_2.svg?style=social)
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
python manage.py createcachetable
python manage.py migrate
python manage.py loaddata initial_groups.json
python manage.py loaddata initial_users.json

```
> run server
```python
python manage.py runserver
```

---
## Additonal Info
![Contrib](https://img.shields.io/github/contributors/cartologic/cartoview_2.svg)
![Languages](https://img.shields.io/github/languages/top/cartologic/cartoview_2.svg)
![License](https://img.shields.io/github/license/cartologic/cartoview_2.svg)