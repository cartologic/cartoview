.. _installation_index:

============
Installation
============

Windows Installation
====================

How to install Cartoview on Windows.

Cartoview requires PostGIS and GeoNode

#. Install PostGIS. We recommend to install Opengeosuite version 4.6 or later which includes PostGIS. If you already have PostGIS installed please go to the next step.

#. Make sure your PostGIS is running, (Programs Files>OpenGeoSuite > Start PostGIS).

#. Download the Windows Installer of `Cartoview <http://www.cartologic.com/cartoview2/download>`_ which includes Geonode.

#. Install Cartoview

* This installer contains GeoNode 2.4 and Cartoview 0.9.14 
* Cartoview has been tested with PostGIS 2.1 and GeoNode 2.4

Installation of multiple instances
==================================

How to install multiple instances of cartoview on the same machine.


Expose localhot to the Internet
===============================

Use `ngrok <https://www.ngrok.com/>`_ to expose local web developent server to the internet.

ngrok is a reverse proxy that creates a secure tunnel from a public endpoint to a locally running web service. 
ngrok captures and analyzes all traffic over the tunnel for later inspection and replay.

For more information visit `GitHub <https://github.com/inconshreveable/ngrok>`_


Deployment for Production
=========================

Text related to the production deployment

.. toctree::
	:maxdepth: 10
	
	deployment/index