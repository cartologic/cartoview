import os

from setuptools import setup
from setuptools import find_packages
try:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:
    from pip.req import parse_requirements
    from pip.download import PipSession
CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Package dependencies
session = PipSession()
install_reqs = parse_requirements(
    os.path.join(CURRENT_DIR, "requirements.txt"), session=session)
reqs = [str(ir.req) for ir in install_reqs]

# Testing dependencies
testing_extras = []

# Documentation dependencies
documentation_extras = []

setup(
    name='cartoview_2',
    version=__import__('cartoview').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    description='A GIS Web Mapping Application Market. Create, share, and visualize GIS Web Mapping Applications',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/cartologic/cartoview_2/',
    author='cartologic',
    author_email='cartoview@cartologic.com',
    keywords=['cartoview', 'gis', 'django', 'web mapping',
              'geonode', 'application management'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development',
    ],
    install_requires=reqs,
    extras_require={
        'testing': testing_extras,
        'docs': documentation_extras
    },
)
