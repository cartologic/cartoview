.. _installation_index:

==================
Installation Guide
==================

The following is a guide to get Cartoview and Geonode up and running in most common operating systems (Windows, Linux/Ubuntu).

Recommended Minimum System Requirements
=======================================

For deployment of Cartoview on a single server, the following are the bare minimum system requirements as per Geonode's documentation. `Here <http://docs.Geonode.org/en/master/tutorials/install_and_admin/quick_install.html>`_

Windows Installation
====================

Pre Installation
================

.. note::
   Cartoview requires PostgreSQL and PostGIS to be installed.
   If you already have PostgreSQL/PostGIS release 9.3 or later installed please proceed to step 2.

#. Download and Install PostgreSQL and PostGIS. 

   Download the installer of PostgreSQL from `EnterpriseDB <http://www.enterprisedb.com/products-services-training/pgdownload#windows>`_. Recommended release is 9.3 or later 32 bits or 64 bits. Please choose the one that is compatible with your system.
   
   .. figure:: ../img/EnterpriseDB_PostgreSQL_Download.png

         *Download PostgreSQL*

   The installation process is straight forward. Just run the downloaded installer, follow the wizard instructions and accept all the default parameters.

   .. figure:: ../img/postgresql_setup1.png

         *Install PostgreSQL*

   Specify the installation folder

   .. figure:: ../img/postgresql_setup2.png

   Specify the installation data folder

   .. figure:: ../img/postgresql_setup3.png

   Specify the database administrator password

   .. figure:: ../img/postgresql_setup4.png

   .. note:: Keep this password safe because we will need it later during the installation of PostGIS.

   Accept the default port (5432) and click the **Next** button.

   .. figure:: ../img/postgresql_setup5.png
   
   Accept the default locals and click the **Next** button

   .. figure:: ../img/postgresql_setup6.png

   Proceed with the installation, click the **Next** button

   .. figure:: ../img/postgresql_setup7.png 


   When you reach this point the installation of PostgreSQL is completed. Please make sure that the **Stack Builder** check box is checked and click **Finish** to proceed with the installation of PostGIS.

   .. figure:: ../img/postgresql_setup8.png

   		  *PostgreSQL installation completed*

   Select **PostgreSQL 9.4(x64) on port 5432** from the combo box and click Next.

   .. figure:: ../img/stack_builder1.png

   Expand the category **Spatial Extensions**, select and check the **PostGIS 2.2** item from the list, choose the one which is compatible with your system (32 bits or 64 bits).

   .. figure:: ../img/stack_builder2.png

   Review your selection and choose a download directory, then click the **Next** button to begin downloading PostGIS installer.
   
   .. figure:: ../img/stack_builder3.png

   The following dialog will indicate that the downloading of PostGIS installer finished successfully. Click **Next** to start installing PostGIS.

   .. figure:: ../img/stack_builder4.png

   Review the license terms and if you accept them, click on the **I Agree** button to continue with the installation of PostGIS.

   .. figure:: ../img/postgis_setup1.png

   **Create spatial database** is optional, however it is recommended. 

   .. figure:: ../img/postgis_setup2.png

   Specify the PostgreSQL installation location in which PostGIS will be installed.

   .. figure:: ../img/postgis_setup3.png

   Provide the PostgreSQL connection information (The one you saved in previous step).

   .. figure:: ../img/postgis_setup4.png

   Specify the name of the spatial database to be created at the end of the installation process. Accept the default is recommended.

   .. figure:: ../img/postgis_setup5.png

   Just click on the **Yes** button.

   .. figure:: ../img/postgis_setup6.png

   Just click on the **Yes** button.

   .. figure:: ../img/postgis_setup7.png

   Just click on the **Yes** button.

   .. figure:: ../img/postgis_setup8.png

   PostGIS setup was competed successfully. Just click on the **Close** button to return to the Stack Builder.

   .. figure:: ../img/postgis_setup9.png

   Installation of PostgreSQL database and PostGIS spatial extension has been completed successfully. Just click on the **Finish** button to complete the installation process.

   .. figure:: ../img/stack_builder5.png

   .. note:: Verify that your Postgres and PostGIS is running using pgAdminIII.

#. Download and install the latest release of **Java Runtime 64-Bit** from `Oracle <https://www.java.com/en/download/manual.jsp>`_

   .. figure:: ../img/java_runtime1.png

      *Java Runtime installer download page*

   .. figure:: ../img/java_runtime2.png

      *Java Runtime installation wizard*

   A few brief dialogs confirm the last steps of the installation process. Click Close on the last dialog and this will complete Java installation process. 

   .. figure:: ../img/java_runtime3.png

      *Java Runtime installation completed* 
      
..   .. warning:: Make sure that the JAVA_HOME environment variable exists and points to the installation folder of Java Runtime
    ``e.g. JAVA_HOME = C:\Program Files\Java\jre1.8.0_66``

   Now you are ready to proceed with the installation of Cartoview.|

#. Download the latest release of **Cartoview** Installer from `Cartologic <http://www.cartologic.com/cartoview/download>`_.
   
   .. figure:: ../img/cartoview_setup1.png

Cartoview and Geonode Installation
==================================

.. note:: This installer contains Geonode 2.4 and Cartoview 0.9.14.
          Cartoview has been tested with PostGIS 2.1 and Geonode 2.4

#. Install Cartoview and Geonode

   The installation process is straight forward. Just run the downloaded installer and follow the wizard instructions.

   .. figure:: ../img/cartoview_setup2.png
   
   Specify the PostgreSQL installation folder.

   .. figure:: ../img/cartoview_setup3.png

   Provide PostgreSQL connection information.

   .. figure:: ../img/cartoview_setup4.png

   .. note:: If you are installing everything on one machine then repeat the PostgreSQL related information provided for the previous dialogs. Additional information might needed, if you have the PostgreSQL data hosted on a separated machine. 

   Specify the PostgreSQL installation data folder.

   .. figure:: ../img/cartoview_setup5.png

   Provide PostgreSQL connection information.

   .. figure:: ../img/cartoview_setup6.png

   Specify installation folder for Geonode, however accepting the default is recommended.

   .. figure:: ../img/cartoview_setup7.png

   Select start menu folder, however accepting the default is again recommended.

   .. figure:: ../img/cartoview_setup8.png

   Setup is ready to install Cartoview and Geonode on your machine. Just click the **Install** button and be patient!

   .. figure:: ../img/cartoview_setup9.png

   Setup has finished installing Cartoview and Geonode on your computer. Just click the **Finish** button to launch the home page in your browser.

   .. figure:: ../img/cartoview_setup10.png

      If you eventually manage to reach this page then the installation has been completed successfully. Click the **Start Geonode** button to launch the Geonode and Cartoview site. Sign in as admin/admin and start enjoying the experience of Geonode and Cartoview on Windows platform. Upload and style layers, create metadata, compose maps, create and install Apps using Cartoview etc.

   .. figure:: ../img/cartoview_setup11.png

Deployment for Production
=========================

Windows Firewall Configuration
------------------------------

   Configure Windows Firewall by creating a dedicated rule for configuring the necessary ports needed for the installed software.

   Initially search and launch the **Windows Firewall with Advanced Security** tool and click on the **New Rule** button.

   .. figure:: ../img/firewall_1.png

   Select **Port** as the type of firewall rule to be applied and click **Next**.

   .. figure:: ../img/firewall_2.png

   Specify the protocol and ports to which the rule applies and click **Next**.

   .. figure:: ../img/firewall_3.png

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

   Specify the rule name and description of this rule and click **Finish** to complete the process.

   .. figure:: ../img/firewall_6.png
   

Replace **localhost** with **IP Address** or **Domain Name**
------------------------------------------------------------

#. Apache 2.4

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

#. Geonode 2.4

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
   
#. Tomcat 8.0

   Open the Tomcat Geoserver configuration file ``..\Geonode\Tomcat 8.0\webapps\geoserver\WEB-INF\web.xml``
   
   Replace localhost with IP Address or Domain Name for the highlighted lines.

   .. code-block:: xml
      :linenos:
      :emphasize-lines: 3

      <context-param>
         <param-name>GEONODE_BASE_URL</param-name>
         <param-value>http://localhost/</param-value>
      </context-param>

   Open the Tomcat Geoserver configuration file ``..\Geonode\Tomcat 8.0\webapps\geoserver\data\security\auth\geonodeAuthProvider\config.xml``
   
   Replace localhost with IP Address or Domain Name for the highlighted lines.

   .. code-block:: xml
      :linenos:
      :emphasize-lines: 5

      <org.geonode.security.GeoNodeAuthProviderConfig>
        <id>-54fbcd7b:1402c24f6bc:-7fe9</id>
        <name>geonodeAuthProvider</name>
        <className>org.geonode.security.GeoNodeAuthenticationProvider</className>
        <baseUrl>http://localhost:4040/</baseUrl>
      </org.geonode.security.GeoNodeAuthProviderConfig>

#. Restart Services

   Restart the Windows services

   * GEONODE_APACHE_4040
   * GEONODE_TOMCAT_4041

#. Geoserver

   * Launch Geoserver's home page at ``http://localhost:4040/geoserver/web``
   * Login as admin/geoserver

   .. figure:: ../img/geoserver_config0.png

   * Click on **Global** button

   * Define the **Proxy Base URL** parameter as: ``http://xx.xx.xx.xx:4040/geoserver``

   .. figure:: ../img/geoserver_config1.png

------------

Linux Installation
==================

Follow `Geonode <http://docs.Geonode.org/en/master/tutorials/install_and_admin/index.html>`_ instructions for installing Geonode on your Ubuntu machine.

Get `Cartoview <https://github.com/cartologic/Cartoview>`_ code from GitHub and install it as Django App in the Geonode project.

Installation of multiple instances
==================================

Documentation not available yet!