/**
 * Created by kamal on 7/2/16.
 */

angular.module('cartoview.mapViewerApp').directive('toggleButton', function(urlsHelper) {
  return {
    restrict: 'E',
    scope: {
      toggle: '=',
      title: '@',
      icon: '@'
    },
    templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/toggle-button.html",
    replace: true,
    link: function($scope, elem, attr, ctrl) {
      // console.debug($scope);
    }
  };
});

function DialogController($scope, $mdDialog, appConfig) {

    $scope.title = appConfig.title;
    $scope.abstract = appConfig.abstract;

    $scope.hide = function() {
        $mdDialog.hide();
    };
    $scope.cancel = function() {
        $mdDialog.cancel();
    };
    $scope.answer = function(answer) {
        $mdDialog.hide(answer);
    };
}

angular.module('cartoview.mapViewerApp').directive('aboutButton', function(mapService,urlsHelper, $mdDialog, $mdMedia) {
    return {
        restrict: 'A',
        link:function(scope, element){
            
            var showAboutDialog = function(ev) {
                var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/about-dialog.html",
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose:true,
                    fullscreen: useFullScreen
                });

                scope.$watch(function() {
                    return $mdMedia('xs') || $mdMedia('sm');
                }, function(wantsFullScreen) {
                    scope.customFullscreen = (wantsFullScreen === true);
                });
            };
            element.on('click',showAboutDialog);
        }
    };
});

angular.module('cartoview.mapViewerApp').directive('layersSwitcher',  function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/layers-switcher.html",
        controller: function ($scope, mapService){
            mapService.get().then(function(){
                $scope.overlays = mapService.map.overlays;
            });

        }
    }
});

angular.module('cartoview.mapViewerApp').directive('layersLegend',  function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/layers-legend.html",
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
angular.module('cartoview.mapViewerApp').directive('basemapsSwitcher',  function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/basemaps-switcher.html",
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

angular.module('cartoview.mapViewerApp').directive('zoomBar',  function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/zoom-bar.html",
        controller: function ($scope, mapService) {
            $scope.map = mapService.map;
        }
    }
});



angular.module('cartoview.mapViewerApp').directive('rotationBar',  function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/view/rotation.html",
        controller: function ($scope, mapService) {
            $scope.rotation = 0;
            mapService.get().then(function () {
                mapService.map.olMap.getView().on('change:rotation', function () {
                    $scope.rotation = mapService.map.olMap.getView().getRotation();
                    $scope.$apply()
                })
            });
            $scope.arrowStyle = function () {
                {
                    transform: 'rotate(' + $scope.rotation + 'deg)'
                }
            }
            $scope.resetRotation = function () {
                mapService.map.olMap.getView().setRotation(0);
            }
            $scope.setRotation = function () {
                var r = mapService.map.olMap.getView().getRotation()
                mapService.map.olMap.getView().setRotation(r + 10);
            }

        }
    }
});
