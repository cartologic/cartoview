'use strict';
var mapWidgetApp = angular.module('cartoview.map', [ 'ngeo']);

//mapWidgetApp.config(function(dashboardProvider) {
//    dashboardProvider.widget('mapWidget', {
//        title: 'map',
//        description: 'Display the current temperature of a city',
//        template: '<cartoview-map map-id="{{config.mapId}}" config-url="{{config.configUrl}}"></cartoview-map>',
//        controller: 'MapWidgetController',
//        frameless: true,
//        edit: {
//            templateUrl: '{widgetsPath}/map/edit.html'
//        }
//    });
//});

mapWidgetApp.service("mapService", function($http, $q) {
    var maps = {};
    var initMap = function(map) {
        var config = map.config;
        var sources = {},
            wmsSources = [];
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
        for (var i = 0; i < config.map.layers.length; i++) {
            var layerConfig = config.map.layers[i];
            var layerSourceConfig = config.sources[layerConfig.source];
            var layer = null;
            if (layerSourceConfig.ptype == 'gxp_osmsource') {

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
                        VERSION: '1.1.1',
                        tiled: layerConfig.tiled,
                        STYLES: layerConfig.styles,
                        FORMAT: layerConfig.format,
                        TRANSPARENT: layerConfig.transparent
                    }
                });
                layer = getTileLayer(layerConfig, layerSource);
                wmsSources.push(layerSource)
            }
            if (layer != null) {
                if (layerConfig.fixed) {
                    baseLayers.push(layer);
                } else {
                    overlays.push(layer)
                }
            }
        }
        map.olMap = new ol.Map({
            layers: [new ol.layer.Group({
                    'title': 'Base maps',
                    layers: baseLayers
                }),
                new ol.layer.Group({
                    'title': 'Overlayes',
                    layers: overlays
                })
            ],
            view: new ol.View({
                //projection: projection, //commented because this cause a shift in wms layers position
                center: config.map.center,
                zoom: config.map.zoom
            })
        });
    };


    var get = function(id, url) {
        maps[id] = maps[id] || {};
        if(!maps[id].promise) {
            var deferObj = $q.defer();
            maps[id].deferObj = deferObj;
            maps[id].promise = deferObj.promise;
        }
        if(url) {
            $http.get(url).then(function (response) {
                maps[id].config = response.data;
                initMap(maps[id]);
                maps[id].deferObj.resolve(maps[id]);
            });
        }
        return maps[id];

    };
    return {
        get: get
    }
});
mapWidgetApp.directive('cartoviewMap',  function($http) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        scope:{
            configUrl: "@",
            mapId: "@"
        },

        controller:function($scope, $element, $compile, mapService){
            $scope.map = mapService.get($scope.mapId, $scope.configUrl);
            $scope.map.promise.then(function(){
                var newElement = $compile( '<div ngeo-map="map.olMap" class="map-widget full-size" ></div>' )( $scope );
                $element.parent().append( newElement );
                var size =  {
                    'h': $element.parent().innerHeight,
                    'w': $element.parent().innerWidth
                };
                var updating = false;
                $scope.$watch(function () {
                    if(!updating){
                        size =  {
                            'h': $element.parent().innerHeight,
                            'w': $element.parent().innerWidth
                        };
                    }
                    updating = false;
                    return size;
                }, function() {
                    updating = true;
                    $scope.map.olMap.updateSize();
                });
                $scope.map.olMap.updateSize();
            });
        }
    }
});


mapWidgetApp.controller('MapWidgetController', function($scope) {

});