from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'cartoview',
  packages = find_packages(),
  version = '1.1.7',
  description = 'Cartoview is a GIS web mapping application framework to easily share and deploy apps based on Geonode',
  author = 'Cartologic',
  author_email = 'info@cartologic.com',
  url = 'https://github.com/cartologic/cartoview',
  include_package_data=True,
  keywords = ['cartoview', 'gis', 'geonode', "django", "web mapping", "applications", "apps", "application management"],
  classifiers = [
    "Development Status :: 3 - Alpha",
    "Framework :: Django :: 1.8",
    "Topic :: Scientific/Engineering :: GIS"
  ],
  license="BSD",
  install_requires= [
    "geonode>=2.5.10",
    "django-geonode-client"
  ]
)

