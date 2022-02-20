![Cartoview Logo](../img/cartoview-logo.png)
# Cartoview Project

## Introduction
Cartoview project is the proper way to use a customized version of Cartoview Core. The repository of [cartoview-project](https://github.com/cartologic/cartoview-project) contains a minimal set of files following the structure of a django-project. Cartoview itself will be installed as a requirement of your project.

Inside the project structure, it's possible to extend, replace or modify all Cartoview & GeoNode components (e.g. CSS and other static files, templates, models, etc.) and even register new django apps without touching the original Cartoview & Geonode code.

This guide describes how to install and configure a fresh setup of Cartoview project to run it in [**Development**](#development-mode) mode on **Ubuntu 20.04 LTS** 64-bit clean environment and [**Production**](#production-mode) mode using **Docker**.

Cartoview project follows the convention of GeoNode project, separating each version in a single branch in Git (e.g. 3.1.x, 3.2.x, and so on).

---

## Installation

### Generate the project
Make sure to have python installed, create a python virtual environment and install Django.

```shell
mkvirtualenv --python=python3.8 cartoview_project_venv
pip install Django==3.2
```

Clone [cartoview-project](https://github.com/cartologic/cartoview-project) and use the branch according to the version you want to. Here,  we will use [3.3.x](https://github.com/cartologic/cartoview-project/tree/3.3.x).

```shell
git clone https://github.com/GeoNode/cartoview-project.git -b 3.3.x
```

This will create a folder called `cartoview-project` from which the custom project will be generated.

Generate the project by executing the following command. Make sure to add the name of for your project.

!!! note
    You can call your cartoview-project whatever you like following the naming conventions for python packages as lower case with underscores (_). In the example below, replace `{{ project_name }}` with whatever you would like to name your project.


```shell
django-admin startproject --template=./cartoview-project -e py,sh,md,rst,json,yml,ini,env,sample,properties -n monitoring-cron -n Dockerfile {{ project_name }}
```

This will generate a folder with the name you've added.

!!! note
    You may remove the virtual environment as it's not needed anymore. It's just used to generate the project.

### Development Mode
In this mode, we will generate, configure, and run the custom project generated in [Generate the project](#generate-the-project) section.

!!! note
    Skip this section if you want to run the project using Docker instead.

Follow the same sections available at [installing Cartoview Core for Ubuntu](ubuntu.md) guide:

1. [Installation Requirements](ubuntu.md#installation-requirements)
2. [Database Installation](ubuntu.md#database-installation)
3. [Database Configuration](ubuntu.md#database-configuration)

After following the previously mentioned sections and while activating the virtual environment, navigate inside the generated project.

```shell
cd {{ project_name }}
```

Install the required packages.
```shell
pip install -r requirements.txt
pip install -e .
```

Follow the same sections mentioned below:

1. [Add Cartoview Environment Variables](ubuntu.md#add-cartoview-environment-variables)
2. [Migrate & Load default data](ubuntu.md#migrate-load-default-data)
3. [GeoServer Installation](ubuntu.md#geoserver-installation)

### Production Mode
In this mode, we will generate, configure, and run the custom project generated in [Generate the project](#generate-the-project) section.

Install Docker and Docker Compose if you don't have them in your machine as explained at [installing docker](docker.md#installation-requirements) section.

Navigate inside the generated project.

```shell
cd {{ project_name }}
```

Build Cartoview containers.

```shell
docker-compose build --no-cache
docker-compose up -d
```

Get a cup of coffee and wait until all cartoview containers are built.

---

## Customize the Look and Feel

With `cartoview-project`, you should have control on the appearance of Cartoview as being able to add and customize the available content (e.g. CSS and other static files, templates, models, etc.).

For more information regarding Cartoview & GeoNode theming, please follow [this guide](https://docs.geonode.org/en/master/basic/theme/index.html#geonode-themes) provided by GeoNode.
