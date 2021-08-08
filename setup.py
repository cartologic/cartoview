from distutils.core import setup

from setuptools import find_packages

long_description = open('README.md').read()
setup(
    name='cartoview',
    packages=find_packages(),
    version=__import__('cartoview').get_current_version(),
    description='Cartoview is a GIS web mapping application framework to \
    easily share and deploy apps based on Geonode',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Cartologic',
    author_email='info@cartologic.com',
    url='https://github.com/cartologic/cartoview',
    include_package_data=True,
    keywords=[
        'cartoview', 'gis', 'geonode', "django", "web mapping", "applications",
        "apps", "application management"
    ],
    classifiers=[
        "Development Status :: 4 - Beta", "Framework :: Django :: 1.8",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    license="BSD",
    install_requires=[
        'future', 'geonode==3.2.1',
        'Faker>=0.8.4',
        'cherrypy==11.0.0',
        'cheroot==5.8.3',
        'portalocker==1.3.0'
    ])
