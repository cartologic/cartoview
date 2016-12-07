'use strict';
angular.module('cartoview.mapViewerApp').service("mapService", function($http, $q, urlsHelper, mapConfig) {
    var  map = {
        loading: 0
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
                zoom: config.map.zoom,
                rotation: 0
            }),
            //renderer: 'canvas',
            layers:[new ol.layer.Group({
                layers:baseLayers
            }),
                new ol.layer.Group({
                layers:overlays
            })]
        });
        // initIdentify();
        //initSearch();
    };

    var deferObj = $q.defer();
    var notRequested  = true;
    var get = function() {
        if(notRequested){
            notRequested = false;
            // $http.get(MAP_CONFIG_URL).then(function (response) {
            //     map.config = response.data;
            //     initMap();
            //     deferObj.resolve(map);
            // });
            map.config = mapConfig;
            initMap();
            deferObj.resolve(map);
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
    map.fit = function (geom) {
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
        view.fit(geom, map.olMap.getSize(), {maxZoom:16});
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




    return {
        get: get,
        map: map
    }
});