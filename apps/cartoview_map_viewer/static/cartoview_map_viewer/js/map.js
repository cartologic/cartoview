'use strict';
angular.module('cartoview.map', [ ]);
// ol.Map.prototype.updateSize = function() {
//   var targetElement = this.getTargetElement();
//
//   if (!targetElement) {
//     this.setSize(undefined);
//   } else {
//
//     this.setSize([targetElement.offsetWidth,targetElement.offsetHeight]);
//   }
// };

angular.module('cartoview.map').service("mapService", function($http, $q) {
    var  map = {
        content: {
            results: []
        },
        loading: 0
    };
    Object.defineProperty(map, 'hasContent', {
        get: function() {
            var hasContent = false;
            map.content.results.forEach(function (result) {
                if(result.features && result.features.length > 0){
                    hasContent = true;
                    return false;
                }
            });
            return hasContent;
        }
    });
    map.addContent = function (content) {
        map.content.results.push(content);
    };
    map.clearContent = function () {
        map.content.results = [];
        map.resultsLayer.get('source').clear();
        delete map.selected;
    };
    var initMap = function() {
        var config = map.config;
        var overlays = [],
            baseLayers = [];
        function getTileLayer(layerConfig, layerSource) {
            return new ol.layer.Tile({
                source: layerSource,
                visible: layerConfig.visibility,
                title: layerConfig.title,
                type: layerConfig.fixed ? 'base' : ''
            });
        }
        var order = 1;
        config.map.layers.forEach(function (layerConfig) {
            //var layerConfig = config.map.layers[i];
            var layerSourceConfig = config.sources[layerConfig.source];
            var layer = null;
            if (layerSourceConfig.ptype == 'gxp_olsource') {
                layer = getTileLayer(layerConfig);
            }
            else if (layerSourceConfig.ptype == 'gxp_osmsource') {
                layer = getTileLayer(layerConfig, new ol.source.OSM());
            } else if (layerSourceConfig.ptype === 'gxp_mapquestsource') {
                layer = getTileLayer(layerConfig, new ol.source.MapQuest({
                    layer: layerConfig.name == 'naip' ? 'sat' : 'osm'
                }));
            } else if (layerSourceConfig.ptype === 'gxp_wmscsource') {
                var layerSource = new ol.source.TileWMS({
                    url: layerSourceConfig.url,
                    params: {
                        LAYERS: layerConfig.name,
                        //VERSION: '1.1.1',
                        TILED: true,
                        STYLES: layerConfig.styles,
                        FORMAT: layerConfig.format,
                        TRANSPARENT: layerConfig.transparent
                    }
                    //,
                    // tileLoadFunction:function(imageTile, src) {
                    //
                    //     var extent     = map.olMap.getView().calculateExtent(map.olMap.getSize());
                    //     //extent      = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
                    //     var coordinates = ol.extent.getBottomLeft(extent);
                    //     imageTile.getImage().src = src + "&TILESORIGIN=" + coordinates[0] + "," + coordinates[1];
                    //     console.debug(imageTile.getImage());
                    //     console.debug(imageTile.getImage().src);
                    // }
                });
                layer = getTileLayer(layerConfig, layerSource);
            }

            if (layer != null) {
                layer.set('title', layerConfig.title);
                if (layerConfig.fixed) {
                    baseLayers.push(layer);
                    if(layerConfig.visibility){
                        baseLayers.active = layer;
                    }

                } else {
                    overlays.push(layer);

                }
                Object.defineProperty(layer, 'visible', {
                    configurable: true,
                    get: function() {
                        return layer.getVisible();
                    },
                    set: function(val) {
                        layer.setVisible(val);
                    }
                });
            }
        });
        map.overlays = overlays;
        map.backgrounds = baseLayers;
        map.olMap = new ol.Map({
            controls:[],
            view: new ol.View({
                center: config.map.center,
                zoom: config.map.zoom
            }),
            //renderer: 'canvas',
            layers:[new ol.layer.Group({
                layers:baseLayers
            }),
                new ol.layer.Group({
                layers:overlays
            })]
        });
        map.resultsLayer = new ol.layer.Vector({
            source: new ol.source.Vector(),
            visible: true,
            style: styleResults
        });
        map.olMap.addLayer(map.resultsLayer);
        initIdentify();
        //initSearch();
    };

    var deferObj = $q.defer();
    var notRequested  = true;
    var get = function() {
        if(notRequested){
            notRequested = false;
            $http.get(MAP_CONFIG_URL).then(function (response) {
                map.config = response.data;
                initMap();
                deferObj.resolve(map);
            });
        }
        return deferObj.promise;
    };
    // zoom functions
    map.zoomHome = function () {
        var view = map.olMap.getView();
        if (!view) {
            return;
        }
        var bounce = ol.animation.bounce({
          resolution: view.getResolution() * 2
        });
        var pan = ol.animation.pan({
          source: view.getCenter()
        });
        map.olMap.beforeRender(bounce);
        map.olMap.beforeRender(pan);
        view.setCenter(map.config.map.center);
        view.setZoom(map.config.map.zoom);
    };

    var zoom = function(delta){
        var view = map.olMap.getView();
        if (!view) {
            return;
        }
        map.olMap.beforeRender(ol.animation.zoom({
            'resolution': view.getResolution(),
            'duration': 500
        }));
        view.setZoom(view.getZoom() + delta);
    };
    map.zoomIn = function () {
        zoom(1);
    };
    map.zoomOut = function () {
        zoom(-1)
    };

    //identify
    var initIdentify = function () {
        if(!map.config.identify){ // set default identify config
            var config = {};
            map.overlays.forEach(function (layer) {
                var layerName = layer.get("source").getParams().LAYERS;
                config[layerName] = {}
            });
            map.config.identify = config;
        }
        map.olMap.on('singleclick', function(evt) {
            map.clearContent();
            var view = map.olMap.getView();
            var viewResolution = view.getResolution();
            var resultsVectorSource = map.resultsLayer.get('source');
            resultsVectorSource.clear();
            map.overlays.forEach(function (layer) {
                var source = layer.get('source');
                var layerName = source.getParams().LAYERS;

                if(!layer.visible || !map.config.identify[layerName] ) return;
                var url = source.getGetFeatureInfoUrl(evt.coordinate, viewResolution,
                                view.getProjection(),
                                {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 10});
                if(window.PROXY_URL)
                    url = PROXY_URL + encodeURIComponent(url);
                map.loading++;
                var result = {
                    layer: layer,
                    features: [],
                    title: layer.get('title'),
                    listItemTpl:  map.config.identify[layerName].listItemTpl || "default-list-item-tpl.html"
                };
                map.content.results.push(result);
                var addFeatures = function (features, crs) {
                    features.forEach(function(f) {
                        f.getGeometry().transform('EPSG:' + crs, 'EPSG:3857');
                        f.properties = f.getProperties();
                        delete f.properties[f.getGeometryName()];
                    });
                    resultsVectorSource.addFeatures(result.features);
                };
                $http.get(url).then(function(response) {
                    map.loading--;
                    result.features = new ol.format.GeoJSON().readFeatures(response.data);
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

    };//end initIdentify
    //search
    var initSearch = function () {
        if(!map.config.search){
            var searchConfig = [];
            map.config.search = searchConfig;
            var urls = {};
            map.overlays.forEach(function (layer) {
                var source = layer.get('source');
                var name = source.getParams().LAYERS;
                var url = source.getUrls()[0];
                if(!urls[url])
                    urls[url] = {};
                urls[url][name] = layer;
            });
            angular.forEach(urls, function(layer, url){
                url += "?service=WFS&request=DescribeFeatureType&outputFormat=application/json&version=2.0.0";
                if(window.PROXY_URL){
                    url = window.PROXY_URL + encodeURIComponent(url);
                }
                $http.get(url).then(function (res) {
                    var workspace = res.data.targetPrefix;
                    res.data.featureTypes.forEach(function (featureType) {
                        var name = workspace + ":" + featureType.name;
                        if(url[name]){
                            var fields = [];
                            featureType.properties.forEach(function (property) {
                               if(property.localType == 'string'){
                                   fields.push(property.name);
                               }
                            });
                            searchConfig.push({
                                layer: layer,
                                fields: fields
                            })
                        }

                    });
                })
            });

        }
    };//end initSearch

    //results management
    map.selectFeature = function (feature) {
        if(map.selected){
            map.selected.set('isSelected', false);
        }
        map.selected = feature;
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


    return {
        get: get,
        map: map
    }
});


angular.module('cartoview.map').directive('cartoviewMap',  function(mapService) {
    return {
        restrict: 'A',
        link:function(scope, element){
            mapService.get().then(function () {
                mapService.map.olMap.setTarget(element[0]);
                mapService.map.olMap.updateSize();
            })
        }
    }
});

angular.module('cartoview.map').directive('layersSwitcher',  function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "layers-switcher.html",
        controller: function ($scope, mapService){
            mapService.get().then(function(){
                $scope.overlays = mapService.map.overlays;
            });

        }
    }
});
angular.module('cartoview.map').directive('layersLegend',  function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "layers-legend.html",
        controller: function ($scope, mapService){
            mapService.get().then(function(){
                $scope.overlays = mapService.map.overlays;
                $scope.overlays.forEach(function (layer) {
                    console.debug(layer);
                })
            });

        }
    }
});
angular.module('cartoview.map').directive('basemapsSwitcher',  function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "basemaps-switcher.html",
        controller: function ($scope, $element, $compile, mapService) {
            mapService.get().then(function(){
                var map = mapService.map.olMap;
                $scope.backgrounds = mapService.map.backgrounds;
                var activeBg;
                $scope.setBackground = function () {
                    var layer = $scope.backgrounds.active;
                    if (activeBg==layer) return;
                    layer.visible = true;
                    activeBg.visible = false;
                    activeBg = layer;
                };
                activeBg = $scope.backgrounds.active;
            });

        }
    }
});

angular.module('cartoview.map').directive('zoomBar',  function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "zoombar.html",
        controller: function ($scope, mapService) {
            $scope.map = mapService.map;
        }
    }
});

angular.module('cartoview.map').directive('mapResults',  function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "map-results.html",
        controller: function ($scope, mapService) {
            $scope.map = mapService.map;
        }
    }
});