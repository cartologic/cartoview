angular.module('myApp', ['ngResourceTastypie'])

.config(function($tastypieProvider){

    $tastypieProvider
    .add('provider1', {
        url: 'http://127.0.0.1:8001/api/v1/',
        username: 'admin',
        apikey: '320c4e7da6ed93946f97f51e6f4c8354a098bb6e'
    });

})

.controller('MyCtrl', ['$scope', '$tastypieResource', '$tastypie', function($scope, $tastypieResource, $tastypie){
    
    $scope.Song = new $tastypieResource('song', {limit:5});
    $scope.Song.objects.$find();    
    $scope.Api = $tastypie;
    $scope.song = $scope.Song.objects.$create();
    
}]);
