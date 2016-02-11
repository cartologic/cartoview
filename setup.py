import os
from setuptools import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="cartoview",
    version="0.2",
    author="",
    author_email="",
    description="cartoview, based on GeoNode",
    long_description=(read('README.md')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="cartoview geonode django",
    url='https://github.com/cartoview/cartoview',
    packages=['cartoview',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'geonode==2.4',
    ]
)
