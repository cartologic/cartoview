/**
 * Created by kamal on 5/9/2016.
 */
window.angularAppDependencies = window.angularAppDependencies || [];
var newInstanceApp = angular.module('newInstanceApp', ['ui.bootstrap', 'ngResourceTastypie'].concat(window.angularAppDependencies));
newInstanceApp.config(function($tastypieProvider, $httpProvider){
    $tastypieProvider.setResourceUrl(REST_URL);
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

newInstanceApp.service("dataService", function ($http, $tastypieResource) {

    //for post save
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
    var maps = new $tastypieResource('geonodemap', {limit: 8});
    var selected = {};
    var instanceObj = {
        config: {}
    };
    var newInstance = true;
    if(window.instanceId){
        newInstance = false;
        var instances = new $tastypieResource('appinstances');
        instances.objects.$get({id:window.instanceId}).then(function(result){
            instanceObj.title = result.title;
            instanceObj.abstract = result.abstract;
            instanceObj.thumbnail_url = result.thumbnail_url;
            try{
                var config = JSON.parse(result.config);
                angular.extend(instanceObj.config, config)
            }
            catch(err){}
            selectMap(result.map);
        },
        function(error){
            console.log(error);
        });
    }



    var save = function () {
        var data = {
            title:instanceObj.title,
            abstract:instanceObj.abstract,
            map: selected.map.id,
            config: JSON.stringify(instanceObj.config)
        };
        var promise = $http.post('', $.param(data));
        return promise;
    };
    var mapSelectCallbacks = [];
    var onMapSelect = function (callback) {
        mapSelectCallbacks.push(callback);
        if(selected.map) callback;
    };

    var selectMap = function (map) {
        if(map == selected.map) return;
        selected.map = map;
        if(newInstance){
            instanceObj.title = map.title;
            instanceObj.abstract = map.abstract;
        }
        angular.forEach(mapSelectCallbacks,function (callback) {
            callback(map);
        });
    };

    return {
        newInstance: newInstance,
        maps: maps,
        selected: selected,
        instanceObj: instanceObj,
        save: save,
        selectMap: selectMap,
        onMapSelect: onMapSelect
    }
});

newInstanceApp.controller('FormController',function($scope, dataService,$tastypieResource, $tastypie, $uibModal){
    $scope.selected = dataService.selected;
});
angular.module('newInstanceApp').directive('mapSelectorField', function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "map-selector-field.html",
        controller: function($scope, $element, $compile, $uibModal, dataService) {
            $scope.selected = dataService.selected;
            $scope.openMapsSelector = function () {
                var modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: 'map-selector-modal.html',
                    controller: 'MapSelectorModalController',
                    size: 'lg'
                });
                // modalInstance.result.then(function (selectedMap) {
                //     $scope.selectedMap = selectedMap;
                // }, function () {
                //     // $log.info('Modal dismissed at: ' + new Date());
                // });
            };
            if(dataService.newInstance){
                $scope.openMapsSelector();
            }
        }
    }
});
newInstanceApp.controller('MapSelectorModalController', function ($scope, dataService, $uibModalInstance) {
    $scope.maps = dataService.maps;
    $scope.maps.objects.$find();
    $scope.selected = {
        map: dataService.selected.map
    };
    $scope.showCancel =  !dataService.newInstance || dataService.selected.map != undefined;
    $scope.ok = function () {
        if($scope.selected.map){
            dataService.selectMap($scope.selected.map);
            $uibModalInstance.close($scope.selected.map);
        }
        else{
            alert("You have to select a map first");
        }
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
angular.module('newInstanceApp').directive('basicFields', function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "basic-fields.html",
        controller: function($scope, dataService) {
            $scope.instanceObj = dataService.instanceObj;
        }
    }
});
angular.module('newInstanceApp').directive('configField', function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "config-field.html",
        controller: function($scope, dataService) {
            $scope.config = JSON.stringify(dataService.instanceObj.config);
            $scope.changeConfig = function () {
                try{
                    dataService.instanceObj.config = JSON.parse($scope.config);
                }
                catch (err){}

            }
        }
    }
});


angular.module('newInstanceApp').directive('saveButtons', function() {
    return {
        restrict: 'E',
        transclude: true,
        replace: true,
        templateUrl: "save-buttons.html",
        controller: function($scope, dataService) {
            //TODDO add details url and view url here
            angular.extend($scope,{
                saving: false,
                success:false,
                error:false,
                errorMsg: "Error!"
            });
            $scope.save = function () {
                $scope.saving = true;
                $scope.error = false;
                $scope.success = false;
                dataService.save().then(function (res) {
                    $scope.success = true;
                    $scope.saving = false;
                    if(res.data.success){
                        if(dataService.newInstance){
                            var editUrl = "edit/" + res.data.id + "/";
                            if(window.location.pathname.lastIndexOf("/") == window.location.pathname.length-1){
                                editUrl = "../" + editUrl;
                            }
                            window.location = editUrl;
                        }
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