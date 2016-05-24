(function () {
var app = angular.module('cartoview.mapViewerApp', ['cartoview.map', 'ngMaterial']);
app.controller('cartoview.mapViewerController', function($scope, $mdSidenav, mapService, $mdMedia, $mdDialog){
    $scope.toggleSidenav = function() {
        return $mdSidenav('left').toggle();
    };
    $scope.map = mapService.map;
    mapService.get().then(function () {
        $scope.title = mapService.map.config.about.title;
        $scope.abstract = mapService.map.config.about.abstract;
    });
    $scope.showAboutDialog = function(ev) {
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
        $mdDialog.show({
            controller: DialogController,
            templateUrl: 'about-dialog.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose:true,
            fullscreen: useFullScreen
        });

        $scope.$watch(function() {
            return $mdMedia('xs') || $mdMedia('sm');
        }, function(wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
        });
    };
});

function DialogController($scope, $mdDialog, mapService) {
    mapService.get().then(function () {
        $scope.title = mapService.map.config.about.title;
        $scope.abstract = mapService.map.config.about.abstract;
    });
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

app.directive('searchBox', function() {
    return {
        restrict: 'E',
        templateUrl: 'search-box.html',
        replace: true,
        controller: function($scope, $element, $compile, mapService) {

        }
    };
});
app.directive('toggleButton', function() {
  return {
    restrict: 'E',
    scope: {
      toggle: '=',
      title: '@',
      icon: '@'
    },
    templateUrl: 'toggle-button.html',
    replace: true,
    link: function($scope, elem, attr, ctrl) {
      // console.debug($scope);
    }
  };
});

})();