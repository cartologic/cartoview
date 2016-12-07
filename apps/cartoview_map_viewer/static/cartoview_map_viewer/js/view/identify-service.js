/**
 * Created by kamal on 7/2/16.
 */
angular.module('cartoview.mapViewerApp').service('identifyService', function(mapService, urlsHelper, $http) {
    var DEFAULT_ITEM_TPL = urlsHelper.static + "cartoview_map_viewer/angular-templates/view/default-list-item-tpl.html"
    var service = this;
    service.content = {
        results: []
    };
    var map = mapService.map;
    service.loading = 0;
    Object.defineProperty(this, 'hasContent', {
        get: function() {
            var hasContent = false;
            service.content.results.forEach(function (result) {
                if(result.features && result.features.length > 0){
                    hasContent = true;
                    return false;
                }
            });
            return hasContent;
        }
    });
    service.clearContent = function () {
        service.content.results = [];
        service.resultsLayer.get('source').clear();
        delete service.selected;
    };
    //results management
    service.selectFeature = function (feature) {
        if(service.selected){
            service.selected.set('isSelected', false);
        }
        service.selected = feature;
        if(feature){
            feature.set('isSelected', true);
        }
    };

    var defaultPointStyle = new ol.style.Style({
        image: new ol.style.Circle({
            // fill: new ol.style.Fill({
            //     color: '#ff0000'
            // }),
            stroke: new ol.style.Stroke({
                color: '#000088',
                width: 2
            }),
            radius: 6
        })
    });
    var defaultPolygonStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#000088',
            width: 2
        })
    });
    var selectedPointStyle = new ol.style.Style({
        image: new ol.style.Circle({
            fill: new ol.style.Fill({
                color: '#ffccff'
            }),
            stroke: new ol.style.Stroke({
                color: '#ffffff'
            }),
            radius: 6
        })
    });
    var selectedPolygonStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#880000',
            width: 3
        })
    });

    var styleResults = function (feature) {
        var polygonStyle = defaultPolygonStyle, pointStyle = defaultPointStyle;
        if(feature.get('isSelected')){
            polygonStyle = selectedPolygonStyle;
            pointStyle = selectedPointStyle;
        }
        return [polygonStyle, pointStyle];
    };
    mapService.get().then(function () {
        if(!map.config.identify) { // set default identify config
            var config = {};
            map.overlays.forEach(function (layer) {
                var layerName = layer.get("source").getParams().LAYERS;
                config[layerName] = {}
            });
            map.config.identify = config;
        }
        service.resultsLayer = new ol.layer.Vector({
            source: new ol.source.Vector(),
            visible: true,
            style: styleResults
        });
        map.olMap.addLayer(service.resultsLayer);

        map.olMap.on('singleclick', function(evt) {
            service.clearContent();
            var view = map.olMap.getView();
            var viewResolution = view.getResolution();
            var resultsVectorSource = service.resultsLayer.get('source');
            resultsVectorSource.clear();
            map.overlays.forEach(function (layer) {
                var source = layer.get('source');
                var layerName = source.getParams().LAYERS;

                if(!layer.visible || !map.config.identify[layerName] ) return;
                var url = source.getGetFeatureInfoUrl(evt.coordinate, viewResolution,
                                view.getProjection(),
                                {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 10});
                if(urlsHelper.proxy)
                    url = urlsHelper.proxy + encodeURIComponent(url);
                service.loading++;
                var result = {
                    layer: layer,
                    features: [],
                    title: layer.get('title'),
                    listItemTpl:  map.config.identify[layerName].listItemTpl || DEFAULT_ITEM_TPL
                };
                service.content.results.push(result);
                var addFeatures = function (features, crs) {
                    features.forEach(function(f) {
                        f.getGeometry().transform('EPSG:' + crs, 'EPSG:3857');
                        f.properties = f.getProperties();
                        delete f.properties[f.getGeometryName()];
                    });
                    resultsVectorSource.addFeatures(result.features);
                    service.featuresCount = resultsVectorSource.getFeatures().length;

                    if(service.featuresCount == 1){

                        service.selectFeature(resultsVectorSource.getFeatures()[0])
                    }
                    else{
                        service.selectFeature()
                    }
                };
                $http.get(url).then(function(response) {
                    service.loading--;
                    result.features = new ol.format.GeoJSON().readFeatures(response.data);
                    if(result.features.length == 0){
                        return;
                    }
                    var crs = response.data.crs.properties.name.split(":").pop();
                    if(proj4.defs('EPSG:' + crs)){
                        addFeatures(result.features, crs );
                    }
                    else{
                        //load the proj def first
                        $http.get("http://epsg.io/?format=json&q=" + crs).then(function (res) {
                            proj4.defs('EPSG:' + crs, res.data.results[0].proj4);
                            addFeatures(result.features, crs);
                        });

                    }

                });//end $http.then
            });//end forEach overlay
        });// end on singleClick
    });
});