How to Create Road Sign inventory Application with Arbiter
==========================================================

The following instructions is to setup road signs inventory layers with customized schema to support drop down selection (domain values).

Instruction
#############
**Note:** Default Geonode_Cartoview installation path and url are used.you can change it according your custom installation.

#. Download and install `Geonode Installer <http://cartologic.com/cartoview2/download>`_  .
#. Login as Admin.
#. Download `application data <https://github.com/cartologic/cartoview_arbiter>`_  which include signs shapefile and schema.xsd file.
#. Open http://localhost:4040/layers/upload and upload  signs shapefile .
#. Copy schema xsd to folder C:\\Program Files (x86)\\Geonode\\Tomcat 8.0\\webapps\\geoserver\\data\\workspaces\\geonode\\datastore\\sign
#. open `geoserver edit layer page <http://localhost:4041/geoserver/web/?wicket:bookmarkablePage=:org.geoserver.web.data.resource.ResourceConfigurationPage&name=sign&wsName=geonode>`_ (you must be logged in as you logged in geonode in step 2) and click "Reload feature type" link at the bottom of the page.
#. Download and install `Arbiter apk <https://s3.amazonaws.com/geoshape-dependencies/Arbiter.apk>`_ .
#. Download `Arbiter user document <https://github.com/ROGUE-JCTD/Arbiter-Android/blob/master/How_to_Use_Arbiter.pdf?raw=true>`_ and follow the instructions to create new project.