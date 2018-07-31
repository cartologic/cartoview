[![GitHub stars](https://img.shields.io/github/stars/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/network)
[![GitHub license](https://img.shields.io/github/license/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/issues)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/cartologic/cartoview.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fcartologic%2Fcartoview)
<p align="center">
  <img src="https://cartologic.github.io/img/cartoview-logo.png"/>
</p>

---
## What is Cartoview?
  - CartoView is a GIS Web Mapping Application Market.
  - Cartoview extends the popular [GeoNode](http://geonode.org/) SDI to provide the ability to create, share, and visualize GIS Web Mapping Applications very easily and very quickly from the browser without programming.

## Docker Installation:
  - install [docker](https://docs.docker.com/v17.12/install/#server) and [docker-compose](https://docs.docker.com/compose/install/#prerequisites)
  - clone cartoview and navigate to cartoview folder
  - on linux based OS use this command `make up` to setup cartoview for the first time 
  - on windows run the following commands to setup cartoview for the first time:
      - `docker-compose up`
      - `docker-compose exec cartoview python manage.py makemigrations`
      - `docker-compose exec cartoview python manage.py migrate`
      - `docker-compose exec cartoview python manage.py loaddata sample_admin.json`
      - `docker-compose exec cartoview python manage.py loaddata json/default_oauth_apps.json`
      - `docker-compose exec cartoview python manage.py loaddata app_stores.json`
      - `docker-compose exec cartoview python manage.py loaddata initial_data.json`
  - open your browser and type the following address `10.5.0.4`

## Docs:
  - [How to use and install](http://cartologic.github.io)
