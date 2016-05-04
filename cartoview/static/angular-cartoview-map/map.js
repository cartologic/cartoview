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
                layer.set('title',layerConfig.title);
                if (layerConfig.fixed) {
                    baseLayers.push(layer);
                } else {
                    overlays.push(layer)
                }
            }
        }
        map.overlays = overlays;
        map.backgrounds = baseLayers;
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
            mapId: "@",
            disableIdentify: "@"
        },

        controller:function($scope, $element, $compile, mapService){
            $scope.disableIdentify = $scope.disableIdentify || false;
            $scope.map = mapService.get($scope.mapId, $scope.configUrl);
            $scope.map.promise.then(function(){
                var tpl = '<div ngeo-map="map.olMap" class="map-widget full-size" >';
                if(!$scope.disableIdentify)
                    tpl += '<map-identify map="map"></map-identify>';
                tpl += '<layer-switcher map="map"></layer-switcher>';
                tpl += '</div>';
                var newElement = $compile( tpl )( $scope );
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
mapWidgetApp.directive('mapIdentify',  function($http) {
    var selectedPointStyle = new ol.style.Style({
        image: new ol.style.Circle({
            fill: new ol.style.Fill({
                color: '#ff0000'
            }),
            stroke: new ol.style.Stroke({
                color: '#ffccff'
            }),
            radius: 8
        })
    });
    var selectedPolygonStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#ff0000',
            width: 2
        })
    });
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        scope:{
            map: "="
        },

        controller:function($scope, $element, $compile, $templateRequest){
            var map = $scope.map.olMap;
            $scope.popup = new ol.Overlay({
                element: $("<div/>").get(0)
            });
            var highlightSource =new ol.source.Vector();
            var highlightOverlay = new ol.layer.Vector({
                source: highlightSource,
                visible: true,
                style: function(feature){ return [ selectedPolygonStyle]; }
            });
            map.addLayer(highlightOverlay);
            map.addOverlay($scope.popup);
            var lastCoordinate;
            var hidePopup = function () {
                var element = $scope.popup.getElement();
                $(element).popover('destroy');
            };
            var updatePopup = function (coordinate) {
                if($scope.features.length == 0) return;
                highlightSource.clear();
                highlightSource.addFeatures([$scope.features[$scope.selected].olFeature]);
                coordinate = coordinate || lastCoordinate;
                lastCoordinate = coordinate;
                $templateRequest('/static/angular-cartoview-map/popup.html').then(function(html){
                    var element = $scope.popup.getElement();
                    $(element).popover('destroy');
                    $scope.popup.setPosition(coordinate);
                    $(element).popover({
                        'placement': 'top',
                        'animation': false,
                        'html': true,
                        //title: $scope.selectedItem.title,
                        'content': $compile(html)($scope),
                        template:'<div class="popover popup-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
                    });

                    $(element).on('shown.bs.popover',function () {
                        var pixel = map.getPixelFromCoordinate(coordinate);
                        // get DOM element generated by Bootstrap
                        var bs_element = $(element).next("div.popover");
                        var offset_height = 10;
                        // get computed popup height and add some offset
                        var popup_height = bs_element.height() + offset_height;
                        // how much space (height) left between clicked pixel and top
                        var height_left = pixel[1] - popup_height;
                        var view = map.getView();
                        // get the actual center
                        var center = view.getCenter();

                        if (height_left < 0) {
                            var center_px = map.getPixelFromCoordinate(center);
                            var new_center_px = [
                                center_px[0],
                                center_px[1] + height_left
                            ];

                            map.beforeRender(ol.animation.pan({
                                source: center,
                                start: Date.now(),
                                duration: 300
                            }));
                            view.setCenter(map.getCoordinateFromPixel(new_center_px));
                        }
                    });
                    $(element).popover('show');

                });
            };
            map.on('singleclick', function(evt) {
                hidePopup();
                $scope.selected = 0;
                $scope.features = [];

                var view = map.getView();
                var viewResolution = view.getResolution();

                angular.forEach($scope.map.overlays, function (layer, index) {
                    var source = layer.get('source');
                    $scope.loadingFeatureList = true;
                    var url = source.getGetFeatureInfoUrl(evt.coordinate, viewResolution,
                                    view.getProjection(),
                                    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 10});
                    if(window.PROXY_URL)
                        url = PROXY_URL + encodeURIComponent(url);

                    $http.get(url).then(function(response) {
                        $scope.loadingFeatureList = false;
                        var features = new ol.format.GeoJSON().readFeatures(response.data);
                        angular.forEach(features, function(f, index){
                            var feature = {};
                            feature.title = f.getId();
                            var geometryName = f.getGeometryName();
                            var properties = f.getProperties();
                            feature.properties = [];
                            feature.olFeature = f;
                            f.getGeometry().transform('EPSG:4326','EPSG:3857');
                            for (var key in properties){
                                if(key == geometryName) continue;
                                feature.properties.push({name: key, value: properties[key]})
                            }
                            $scope.features.push(feature);
                        });//end forEach feature

                        updatePopup(evt.coordinate);
                    });//end $http.then
                });//end forEach overlay

                /////////////////



                ////////////////////

            });// end on singleClick

            $scope.goPrev = function () {
                if($scope.selected > 0){
                    $scope.selected--;
                    updatePopup();
                }
            };
            $scope.goNext = function () {
                if($scope.selected < $scope.features.length - 1){
                    $scope.selected++;
                    updatePopup();
                }
            };
            $scope.closePopup = function () {
                $scope.selected = 0;
                $scope.features = [];
                highlightSource.clear();
                hidePopup();
            };

        }
    }
});

mapWidgetApp.controller('MapWidgetController', function($scope) {

});

mapWidgetApp.directive('layerSwitcher',  function($http) {
    var layersSwitcherControl = function(opt_options) {
        var options = opt_options || {};
        var button = document.createElement('button');
        button.innerHTML = '<span class="glyphicon glyphicon-menu-hamburger"></span>';
        var element = document.createElement('div');
        element.className = 'layers-switcher ol-unselectable ol-control';
        element.appendChild(button);
        ol.control.Control.call(this, {
            element: element,
            target: options.target
        });
    };
    ol.inherits(layersSwitcherControl, ol.control.Control);

    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        scope: {
            map: "="
        },
        controller: function ($scope, $element, $compile, $templateRequest, ngeoBackgroundLayerMgr, ngeoDecorateLayer) {
            var map = $scope.map.olMap;
            var control = new layersSwitcherControl();
            map.addControl(control);
            $scope.layers = [];
            $scope.overlays = $scope.map.overlays;
            $scope.backgrounds = $scope.map.backgrounds;
            var activeBg;
            $scope.setBackground = function (layer) {
                if (activeBg==layer) return;
                layer.visible = true;
                activeBg.visible = false;
                activeBg = layer;
            };
            angular.forEach($scope.map.backgrounds, function (layer) {
                ngeoDecorateLayer(layer);
                if(layer.visible){
                    $scope.backgrounds.active = activeBg = layer;
                }
            });
            angular.forEach($scope.map.overlays,function (layer) {
                ngeoDecorateLayer(layer);
            });
            map.getLayers().forEach(function (layer) {
                if(!layer.getLayers){
                    ngeoDecorateLayer(layer);
                    $scope.layers.push(layer);
                }
            });
            $templateRequest('/static/angular-cartoview-map/layers-switcher.html').then(function(html) {
                var btn = $(control.element).find('button');
                btn.popover({
                    'placement': 'left',
                    'animation': false,
                    'html': true,
                    'content': $compile(html)($scope),
                    template:'<div class="popover layers-switcher-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
                });
            });

        }
    }
});