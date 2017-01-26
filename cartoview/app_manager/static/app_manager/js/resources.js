(function(){
    var app = angular.module('cartoview.appManager.resources',['cartoview.urlsHelper', 'cartoview.userInfo', "ngResource"]);
    app.config(function($httpProvider, $resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        // $resourceProvider.defaults.stripTrailingSlashes = false;
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.service("InstalledAppResource", function(urls, $resource){
        return $resource(urls.REST_URL + 'app/', {}, {
            'query': {
                isArray: false
            }
        });
    });

    app.service("AppStoreResource", function(urls, $resource){
        return $resource(urls.REST_URL + 'appstore/:storeId', {storeId:'@id'}, {
            'query': {
                isArray: false
            }
        });
    });

    app.service("AppStore", function(urls, $resource){
        function AppResource(store){
            return $resource(store.url + 'app/:storeId', {storeId:'@id'}, {
                'query': {
                    isArray: false,
                    method: 'JSONP',
                    params: {callback: 'JSON_CALLBACK'}
                }
            });
        }
        return {
            AppResource: AppResource
        }
    });


})();