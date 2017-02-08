(function(){
    var app = angular.module('cartoview.appManager.resources',['cartoview.urlsHelper', 'cartoview.userInfo', "ngResource"]);
    app.config(function($httpProvider, $resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.service("InstalledAppResource", function(urls, $resource){
        var resourceUrl = urls.REST_URL + 'app/:appId/:action/';
        return $resource(resourceUrl, {}, {
            'query': {
                isArray: false
            },
            suspend:{
                isArray: false,
                method: 'POST',
                params:{
                    action: "suspend",
                    appId: "@appId"
                }
            },
            activate: {
                isArray: false,
                method: 'POST',
                params:{
                    action: "activate",
                    appId: "@appId"
                }
            },
            reorder:{
                isArray: false,
                method: 'POST',
                params:{
                    action: "reorder"
                }
            },
            install:{
                isArray: false,
                method: 'POST',
                params:{
                    action: "install"
                }
            },
            uninstall: {
                isArray: false,
                method: 'POST',
                params:{
                    action: "uninstall",
                    appId: "@appId"
                }
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