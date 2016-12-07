/**
 * Created by kamal on 6/28/16.
 */
angular.module('cartoview.viewer.editor').directive('widgetConfig', function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        scope:{
            widgetName: "@"
        },
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/edit/widget-config.html",
        controller: function($scope, dataService, widgetsInfo) {
            $scope.instanceObj = dataService.instanceObj;
            $scope.instanceObj.config.widgets = $scope.instanceObj.config.widgets || {};
            $scope.widget = widgetsInfo.get($scope.widgetName);
        }
    }
});
