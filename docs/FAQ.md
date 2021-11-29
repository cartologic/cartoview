![Cartoview Logo](img/cartoview-logo.png)
# Frequently Asked Questions

**1. What is Cartoview exactly? Is it a replacement for GeoNode?**
    
[Cartoview](https://cartoview.net/) is a [Geo App market](https://appstore.cartoview.net/) for GeoNode. It is not a fork / improvement / reprlacement of GeoNode, but rather additional code aimed to make it more extensible to integrate third party apps directly from the browser.

***

**2. What are the goals of Cartoview?**

- Sharing GIS Apps.
- Provide apps for common tasks like visualizing and querying feature services.
- Extend the functions of the GeoNode SDI beyond data management.
- Provide a solid core of utilities that can be used to help developers integrate and deploy their Geo apps.
- Foster an ecosystem of apps extending easily deplyable and installable.

***

**3. Can I use Cartoview with GeoNode Version 2.4 and earlier?**

Cartoview starts working with GeoNode 2.5

***

**4. I have an idea! What should I do?**

Please [file an issue](https://github.com/cartologic/cartoview/issues/new). Issues are a great way to discuss new ideas, build consensus, and talk about implementation details.

***

**5. I built something with Cartoview, can I show you?**

Absolutely! Share it on Twitter with [@ahmednosman](https://twitter.com/ahmednosman) or [@Cartoview](https://twitter.com/CartoView).

***

**6. I built a reusable app can I contribute it?**

Of course! This is the purpose of Cartoview. Read the instructions on developing and deploying apps. Create an account on [Cartoview App market](https://appstore.cartoview.net/) and load your app. Your app will be immediately available to all Cartoview deployments.

***

**7. What are the best Cartoview Apps?**

- [ArcGIS Importer](https://appstore.cartoview.net/app/arcgis_importer/): This app allows importing ArcGIS feature layer into a PostGIS database while adding it to GeoServer and GeoNode.

- [Data Manager](https://appstore.cartoview.net/app/data_manager/): Upload and puplish a [GeoPackage](https://www.geopackage.org/) to GeoServer and GeoNode.

- [Terria Map](https://appstore.cartoview.net/app/cartoview_terriaJs/): Visulaize GeoNode maps using a library for building rich, web-based geospatial data platforms called [TerriaJS](https://terria.io/).

- (Coming Soon) **Data Collection**: This app enables you to collect data through dynamically configured forms using mobile app and add them as features to an empty layer in GeoNode.

***

**8. Running Cartoview on GeoNode and QGIS Server?**

There is no reason for Cartoview not to work on this deployment. (This was never tested). Apps relying on GeoServer of course will not work.
