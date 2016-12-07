/**
 * Created by kamal on 7/2/16.
 */

angular.module('cartoview.mapViewerApp').directive('cartoviewMap',  function(mapService, $timeout) {
    return {
        restrict: 'A',
        link: function (scope, element) {
            mapService.get().then(function () {
                mapService.map.olMap.setTarget(element[0]);
                mapService.map.olMap.updateSize();
                scope.$watch(function () {
                        return [element[0].offsetWidth, element[0].offsetHeight].join('x');
                    },
                    function (value) {
                        mapService.map.olMap.updateSize();
                    });
                // $timeout(function () {
                //     mapService.map.olMap.updateSize();
                // }, 500)
            })
        }
    }
});