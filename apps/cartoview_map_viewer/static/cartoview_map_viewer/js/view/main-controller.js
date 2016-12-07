/**
 * Created by kamal on 7/2/16.
 */

angular.module('cartoview.mapViewerApp').controller('cartoview.MainController',
    function($scope, mapService, identifyService, $mdSidenav, $mdMedia, $mdDialog, appConfig){
        $scope.config = appConfig;
        console.debug(appConfig)
        console.debug("==============================")
        $scope.toggleSidenav = function() {
            return $mdSidenav('left').toggle();
        };
        $scope.map = mapService.map;
        $scope.identify = identifyService;

        // mapService.get().then(function () {
        //     $scope.title = mapService.map.config.about.title;
        //     $scope.abstract = mapService.map.config.about.abstract;
        // });
        //
    });