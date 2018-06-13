angular.module('myApp', ['ngResourceTastypie', 'ngMaterial', 'ui.bootstrap', 'ngMdIcons', 'jsonFormatter'])

.config(function($tastypieProvider, $mdThemingProvider){
    $tastypieProvider.setResourceUrl('http://127.0.0.1:8001/api/v1/');
    $tastypieProvider.setAuth('admin','320c4e7da6ed93946f97f51e6f4c8354a098bb6e');
})

.service('Api', ['$tastypie', '$tastypieResource', function($tastypie, $tastypieResource){
    this.Provider = $tastypie;
    this.Song = new $tastypieResource('song', {limit:4});
    this.Song.objects.$find();
}])

.controller('ProjectCtrl', ['$scope', '$mdSidenav', 'Api', function($scope, $mdSidenav, Api){
    $scope.toggleSidenav = function(menuId){
        $mdSidenav(menuId).toggle();
    };
    $scope.Api = Api;
}])

.controller('SongCtrl', function ($scope, $timeout, $mdSidenav, $mdUtil, $log, Api){
    $scope.Song = Api.Song;
    
    $scope.select = function(obj){
        if(typeof(obj) == 'undefined') return;
        if(!obj) return;
        $scope.rightTitle = ((obj.id > 0) ? 'Edit Song' : 'New Song');
        $scope.song = obj;
        $scope.toggleRight();
    };
    
    $scope.new = function(){
        var song = Api.Song.objects.$create();
        $scope.select(song);
    };
    
    $scope.toggleRight = buildToggler('right');    
    function buildToggler(navID){
      var debounceFn = $mdUtil.debounce(function(){
            $mdSidenav(navID)
              .toggle()
              .then(function(){
                $log.debug("toggle " + navID + " is done");
              });
          },300);
      return debounceFn;
    }
})

.controller('RightCtrl', function ($scope, $timeout, $mdSidenav, $log) {
    $scope.close = function(){
        $mdSidenav('right').close().then(function(){
          $log.debug("close RIGHT is done");
        });
    };
    
    $scope.save = function(obj){
        obj.$save().then(
            function(){
                $scope.close();
            }
        );
    };
    
    $scope.delete = function(obj){
        obj.$delete().then(
            function(){
                $scope.close();
            }
        );
    };
});