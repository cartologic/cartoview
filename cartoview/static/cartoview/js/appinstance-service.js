/**
 * Created by kamal on 8/4/16.
 */
angular.module('cartoview.appInstances', ['ngResource', 'cartoview.urlsHelper']);
angular.module('cartoview.appInstances').config(function ($httpProvider) {
    $httpProvider.defaults.withCredentials = true
});
angular.module('cartoview.appInstances').factory('AppInstance', function ($resource, urls) {
    return $resource(urls.REST_URL + 'appinstances/:instanceId/', {instanceId: '@id'}, {
        update: {
            method: 'PUT'
        }
    });
});