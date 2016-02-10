.. _installation_index:

Installation Guide
==================

The following is a guide to get Geonode and Cartoview up and running in most common operating systems (Windows, Linux/Ubuntu).

Recommended Minimum System Requirements
---------------------------------------

For the deployment of Geonode and Cartoview on a single server, please find the bare minimum system requirements in Geonode's `Documentation. <http://docs.Geonode.org/en/master/tutorials/install_and_admin/quick_install.html>`_

Windows Installation
--------------------

Pre Installation
~~~~~~~~~~~~~~~~

1. Download and Install PostgreSQL and PostGIS. 

  .. note::
    Cartoview requires PostgreSQL and PostGIS release 9.3 or later to be installed.
    If they are already installed on your system, please proceed to :ref:`Java Installation <java_installation>`.

  Download the installer of PostgreSQL from `EnterpriseDB <http://www.enterprisedb.com/products-services-training/pgdownload#windows>`_. Recommended release is 9.3 or later 32 bits or 64 bits. Please choose the one that is compatible with your system.
   
  .. figure:: ../img/postgresql_setup0.png
     :alt: download postgresql
     :target: http://www.enterprisedb.com/products-services-training/pgdownload#windows
     :width: 380 pt

     *Download PostgreSQL*

  The installation process is straight forward. Just run the downloaded installer, follow the wizard instructions and accept all the default parameters.

  .. figure:: ../img/postgresql_setup1.png
     :width: 350 pt

     *Install PostgreSQL*

  Specify the installation folder

  .. figure:: ../img/postgresql_setup2.png
     :width: 350 pt

  Specify the installation data folder

  .. figure:: ../img/postgresql_setup3.png
     :width: 350 pt

  Specify the database administrator password

  .. figure:: ../img/postgresql_setup4.png
     :width: 350 pt

  .. note:: Keep this password safe because we will need it later during the installation of PostGIS.

  Accept the default port (5432) and click the **Next** button.

  .. figure:: ../img/postgresql_setup5.png
     :width: 350 pt

  Accept the default locals and click the **Next** button

  .. figure:: ../img/postgresql_setup6.png
     :width: 350 pt

  Proceed with the installation, click the **Next** button

  .. figure:: ../img/postgresql_setup7.png 
     :width: 350 pt

  When you reach this point the installation of PostgreSQL is completed. Please make sure that the **Stack Builder** check box is checked and click **Finish** to proceed with the installation of PostGIS.

  .. figure:: ../img/postgresql_setup8.png
     :width: 350 pt

     PostgreSQL installation completed

  Select **PostgreSQL 9.4(x64) on port 5432** from the combo box and click Next.

  .. figure:: ../img/stack_builder1.png
     :width: 350 pt
  
  Expand the category **Spatial Extensions**, select and check the **PostGIS 2.2** item from the list, choose the one which is compatible with your system (32 bits or 64 bits).

  .. figure:: ../img/stack_builder2.png
     :width: 350 pt

  Review your selection and choose a download directory, then click the **Next** button to begin downloading PostGIS installer.
   
  .. figure:: ../img/stack_builder3.png
     :width: 350 pt

  The following dialog will indicate that the downloading of PostGIS installer finished successfully. Click **Next** to start installing PostGIS.

  .. figure:: ../img/stack_builder4.png
     :width: 350 pt

  Review the license terms and if you accept them, click on the **I Agree** button to continue with the installation of PostGIS.

  .. figure:: ../img/postgis_setup1.png
     :width: 350 pt

  **Create spatial database** is optional, however it is recommended. 

  .. figure:: ../img/postgis_setup2.png
     :width: 350 pt

  Specify the PostgreSQL installation location in which PostGIS will be installed.

  .. figure:: ../img/postgis_setup3.png
     :width: 350 pt

  Provide the PostgreSQL connection information (The one you saved in previous step).

  .. figure:: ../img/postgis_setup4.png
     :width: 350 pt

  Specify the name of the spatial database to be created at the end of the installation process. Accept the default is recommended.

  .. figure:: ../img/postgis_setup5.png
     :width: 350 pt

  Just click on the **Yes** button.

  .. figure:: ../img/postgis_setup6.png
     :width: 350 pt

  Just click on the **Yes** button.

  .. figure:: ../img/postgis_setup7.png
     :width: 350 pt

  Just click on the **Yes** button.

  .. figure:: ../img/postgis_setup8.png
     :width: 350 pt

  PostGIS setup was competed successfully. Just click on the **Close** button to return to the Stack Builder.

  .. figure:: ../img/postgis_setup9.png
     :width: 350 pt

  Installation of PostgreSQL database and PostGIS spatial extension has been completed successfully. Just click on the **Finish** button to complete the installation process.

  .. figure:: ../img/stack_builder5.png
     :width: 350 pt
     
  .. note:: Verify that your Postgres and PostGIS is running using pgAdminIII.

.. _java_installation:

2. Download and install the latest release of **Java Runtime 64-Bit** from `Oracle <https://www.java.com/en/download/manual.jsp>`_

  .. note::
    Cartoview requires Java runtime 64-Bit release 7 or later to be installed.
    If it is already installed on your system, please proceed to :ref:`Cartoview Installation <cartoview_installation>`.

  .. figure:: ../img/java_runtime1.png

    *Java Runtime installer download page*

  .. figure:: ../img/java_runtime2.png

    *Java Runtime installation wizard*

    A few brief dialogs confirm the last steps of the installation process. Click Close on the last dialog and this will complete Java installation process. 
  .. figure:: ../img/java_runtime3.png

    *Java Runtime installation completed* 

.. important:: Now you are ready to proceed with the installation of Geonode and Cartoview.

------------

.. _cartoview_installation:

Geonode and Cartoview Installation
----------------------------------

  .. note:: This installer contains Geonode 2.4 and Cartoview 0.9.14.
    Cartoview has been tested with PostGIS 2.1 and Geonode 2.4

  Download the latest release of **Geonode_Cartoview** Installer from `Cartologic <http://www.cartologic.com/cartoview/download>`_.
   
  .. figure:: ../img/cartoview_setup1.png

  The installation process is straight forward. Just run the downloaded installer and follow the wizard instructions. Accepting the defaults is strongly recommented.

  .. figure:: ../img/cartoview_setup2.png

  Specify the PostgreSQL installation folder.

  .. figure:: ../img/cartoview_setup3.png

  Provide PostgreSQL connection information.

  .. figure:: ../img/cartoview_setup4.png

  Provide the Geonode database name. This database will host information related to the Geonode website e.g. users, permissions etc.

  .. figure:: ../img/cartoview_setup5.png

  Provide the GIS database name. This database will host the GIS data.

  .. figure:: ../img/cartoview_setup6.png

  Specify installation folder for Geonode_Cartoview, however accepting the default is recommended.

  .. figure:: ../img/cartoview_setup7.png

  Provide start menu folder name, however accepting the default is again recommended.

  .. figure:: ../img/cartoview_setup8.png

  Setup is ready to install Geonode and Cartoview on your machine. Just click the **Install** button and be patient!

  .. figure:: ../img/cartoview_setup9.png

  Setup has finished installing Geonode and Cartoview on your computer. Just click the **Finish** button to launch the home page in your browser.

  .. figure:: ../img/cartoview_setup10.png

  Congratulations! You have successfully installed Geonode and Cartoview on your machine. This is the Admin Configuration page.
  Click the **Start Geonode** button to launch the Geonode and Cartoview home page.
  
  .. figure:: ../img/cartoview_setup11.png

  Sign in as admin/admin and start enjoying the experience of Geonode and Cartoview on Windows platform. Upload and style layers, create metadata, compose maps, share layers and maps with others, create and install Apps using Cartoview etc.

  .. figure:: ../img/cartoview_setup12.png

Deployment for Production
-------------------------
  .. danger:: Make sure that you have changed the default admin passwords for Django, Apache, Tomcat and Geoserver before you expose your site to the web. All default passwords are listed at the admin page installed with Cartoview.

Windows Firewall Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  .. note:: Cartoview is installed by default on localhost. In order to deploy Cartoview on your production server and make it accessible to other users, you will need to change the hostname and configure all necessary ports. 

Configure Windows Firewall
^^^^^^^^^^^^^^^^^^^^^^^^^^
  Create a new **Inbound Rule** to group the configuration of the necessary ports needed for the installed software.
  Initially, search and launch the **Windows Firewall with Advanced Security** tool and click on the **New Rule** button.

  .. figure:: ../img/firewall_1.png

  Select **Port** as the type of Firewall Rule to be applied and click **Next**.

  .. figure:: ../img/firewall_2.png

  Specify the protocol and ports to which the rule applies and click **Next**.

  .. figure:: ../img/firewall_3.png

  .. tip:: 
    +-----------+------+
    | Software  | Port |
    +===========+======+
    | Geonode   | 4040 |
    +-----------+------+
    | GeoServer | 4041 |
    +-----------+------+
    | PostgreSQL| 5432 |
    +-----------+------+
    | SSL       | 555  |
    +-----------+------+

  Specify the action to be taken when a connection matches the conditions specified in the rule and click **Next**. (Allow the connection) 

  .. figure:: ../img/firewall_4.png

  Specify the profiles for which this rule applies. Accepting the defaults is recommended. Finally click **Next** to proceed to the next step. (All the options checked).

  .. figure:: ../img/firewall_5.png

  Specify the name and description of this rule and click **Finish** to complete the process.

  .. figure:: ../img/firewall_6.png
   
Replace localhost with IP Address or Domain Name
------------------------------------------------

1. Apache 2.4

  Open the Apache configuration file ``..\Goenode\Apache24\conf\httpd.conf``.

  Replace localhost with IP Address or Domain Name only for the highlighted lines.

  .. code-block:: python
    :linenos:
    :emphasize-lines: 12,14

    WSGIPassAuthorization On
    WSGIPythonHome "C:/Program Files (x86)/Geonode/Python"

    <Proxy *>
        Order allow,deny
        Allow from all
    </Proxy>
     
      ProxyRequests     Off
      ProxyPreserveHost On

      ProxyPass /geoserver http://localhost:4041/geoserver max=200 ttl=120 retry=300

      ProxyPassReverse /geoserver http://localhost:4041/geoserver

2. Geonode 2.4

  Open the Geonode configuration file ``..\Geonode\geonode\geonode\local_settings.py``
   
  Replace localhost with IP Address or Domain Name only for the highlighted lines.

  .. code-block:: python
      :linenos:
      :emphasize-lines: 1,7

      SITEURL = "http://localhost:4040/"

      OGC_SERVER = {
          'default' : {
              'BACKEND' : 'geonode.geoserver',
              'LOCATION' : 'http://localhost:4041/geoserver/',
              'PUBLIC_LOCATION' : 'http://localhost:4041/geoserver/',
              'USER' : 'admin',
              'PASSWORD' : 'geoserver',
              'MAPFISH_PRINT_ENABLED' : True,
              'PRINT_NG_ENABLED' : True,
              'GEONODE_SECURITY_ENABLED' : True,
              'GEOGIG_ENABLED' : False,
              'WMST_ENABLED' : False,
              'BACKEND_WRITE_ENABLED': True,
              'WPS_ENABLED' : False,
              'LOG_FILE': '%s/geoserver/data/logs/geoserver.log' % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
              # Set to name of database in DATABASES dictionary to enable
              'DATASTORE': 'datastore',
          }
      }
   
3. Tomcat 8.0

  Open the Tomcat Geoserver configuration file ``..\Geonode\Tomcat 8.0\webapps\geoserver\WEB-INF\web.xml``
   
  Replace localhost with IP Address or Domain Name for the highlighted line.

  .. code-block:: xml
      :linenos:
      :emphasize-lines: 3

      <context-param>
        <param-name>GEONODE_BASE_URL</param-name>
        <param-value>http://localhost/</param-value>
      </context-param>

  Open the Tomcat Geoserver configuration file ``..\Geonode\Tomcat 8.0\webapps\geoserver\data\security\auth\geonodeAuthProvider\config.xml``
   
  Replace localhost with IP Address or Domain Name for the highlighted line.

  .. code-block:: xml
      :linenos:
      :emphasize-lines: 5

      <org.geonode.security.GeoNodeAuthProviderConfig>
        <id>-54fbcd7b:1402c24f6bc:-7fe9</id>
        <name>geonodeAuthProvider</name>
        <className>org.geonode.security.GeoNodeAuthenticationProvider</className>
        <baseUrl>http://localhost:4040/</baseUrl>
      </org.geonode.security.GeoNodeAuthProviderConfig>

4. Restart Services

  Restart the Windows services

    * GEONODE_APACHE_4040
    * GEONODE_TOMCAT_4041

5. Geoserver 2.7.4

  * Launch Geoserver's home page at ``http://localhost:4040/geoserver/web``
  * Login as admin/geoserver

  .. figure:: ../img/geoserver_config0.png

  * Click on **Global** button

  * Define the **Proxy Base URL** parameter as: ``http://xx.xx.xx.xx:4040/geoserver``

  .. figure:: ../img/geoserver_config1.png

------------

Linux/Ubuntu Installation
-------------------------

Follow `Geonode <http://docs.Geonode.org/en/master/tutorials/install_and_admin/index.html>`_ instructions for installing Geonode on your Ubuntu machine.

Get `Cartoview <https://github.com/cartologic/Cartoview>`_ code from GitHub and install it as Django App in the Geonode project.

Installation of multiple instances
----------------------------------

Documentation not available yet!