/**
 * Created by kamal on 8/21/16.
 */
angular.module('cartoview.topToolbar', ['cartoview.urlsHelper','cartoview.userInfo', 'ngMaterial'])
    .directive('cartoviewTopToolbar',  function(urls, cartoviewUser) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urls.STATIC_URL + "cartoview/angular-templates/top-toolbar.html",
        controller: function ($scope, $mdSidenav) {
            $scope.cartoviewUser = cartoviewUser;
            $scope.urls = urls;
            $scope.showMobileMainHeader = true;
            $scope.openSideNavPanel = function(panelId) {
                $mdSidenav(panelId).open();
            };
            $scope.closeSideNavPanel = function(panelId) {
                $mdSidenav(panelId).close();
            };
        }
    }
});