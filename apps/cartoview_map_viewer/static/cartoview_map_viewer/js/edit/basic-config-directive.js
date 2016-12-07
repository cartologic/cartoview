/**
 * Created by kamal on 6/28/16.
 */
angular.module('cartoview.viewer.editor').directive('basicConfig', function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/edit/basic-config.html",
        controller: function($scope, dataService, $mdMedia, $mdDialog) {
            $scope.instanceObj = dataService.instanceObj;
            $scope.selected = dataService.selected;
            
            
        }
    }
});
