/**
 * Created by kamal on 6/28/16.
 */
angular.module('cartoview.viewer.editor').directive('actionsBar', function(urlsHelper) {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: urlsHelper.static + "cartoview_map_viewer/angular-templates/edit/actions-bar.html",
        controller: function($scope, dataService) {
            //TODDO add details url and view url here
            angular.extend($scope,{
                saving: false,
                success:false,
                error:false,
                errorMsg: "Error!",
                newInstance: dataService.newInstance,
                urls: urlsHelper
            });

            $scope.save = function () {
                $scope.saving = true;
                $scope.error = false;
                $scope.success = false;
                dataService.save().then(function (res) {
                    $scope.saving = false;
                    if(res.data.success){
                        $scope.success = true;
                        if(dataService.newInstance){
                            var editUrl = res.data.id + "/edit/";
                            if(window.location.pathname.lastIndexOf("/") == window.location.pathname.length-1){
                                editUrl = "../" + editUrl;
                            }
                            window.location = editUrl;
                        }
                    }
                    else {
                        $scope.error = true;
                        $scope.errorMsg = res.data.error_message;
                    }
                },function (error) {
                    $scope.saving = false;
                    $scope.error = true;
                    $scope.errorMsg = error;
                });
            }

        }
    }
});