/**
 * Created by kamal on 6/28/16.
 */
angular.module('cartoview.viewer.editor').directive('mapSelector', function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/edit/map-selector.html",
        controller: function($scope, dataService, $mdMedia, $mdDialog) {
            $scope.instanceObj = dataService.instanceObj;
            $scope.selected = dataService.selected;
            
            $scope.openMapsSelector = function(ev) {
                var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
                $mdDialog.show({
                controller: MapSelectorDialogController,
                    templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/edit/map-selector-dialog.html?aa",
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose:true,
                    fullscreen: useFullScreen
                }).then(function(answer) {
                    //$scope.status = 'You said the information was "' + answer + '".';
                }, function() {
                    $scope.status = 'You cancelled the dialog.';
                });
                $scope.$watch(function() {
                    return $mdMedia('xs') || $mdMedia('sm');
                }, function(wantsFullScreen) {
                    $scope.customFullscreen = (wantsFullScreen === true);
                });
            };
        }
    }
});

function MapSelectorDialogController($scope, dataService,  $mdDialog) {
    $scope.maps = dataService.maps;
    $scope.maps.objects.$find();
    $scope.selected = {
        map: dataService.selected.map
    };
    $scope.showCancel =  !dataService.newInstance || dataService.selected.map != undefined;
    $scope.ok = function () {
        if($scope.selected.map){
            dataService.selectMap($scope.selected.map);
            $mdDialog.hide($scope.selected.map);
        }
        else{
            alert("You have to select a map first");
        }
    };
    $scope.cancel = function () {
        $mdDialog.cancel();
    };
}