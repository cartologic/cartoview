from distutils.core import setup

from setuptools import find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()
setup(
    name='cartoview',
    packages=find_packages(),
    version=__import__('cartoview').get_current_version(),
    description='Cartoview is a GIS web mapping application framework to \
    easily share and deploy apps based on Geonode',
    long_description=long_description,
    author='Cartologic',
    author_email='info@cartologic.com',
    url='https://github.com/cartologic/cartoview',
    include_package_data=True,
    python_requires='>=2.7.12, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    keywords=[
        'cartoview',
        'gis',
        'geonode',
        "django",
        "web mapping",
        "applications",
        "apps",
        "application management"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django :: 1.8",
        "Topic :: Scientific/Engineering :: GIS"],
    license="BSD",
    install_requires=['future', 'six==1.10.0'])
