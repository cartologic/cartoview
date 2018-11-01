(function () {
    var app = angular.module('cartoview.appManager.resources', ['cartoview.urlsHelper', 'cartoview.userInfo', "ngResource"]);
    app.config(function ($httpProvider, $resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    app.service("InstalledAppResource", function (urls, $resource) {
        var resourceUrl = urls.REST_URL + 'app/:appId/:action/';
        return $resource(resourceUrl, {}, {
            'query': {
                isArray: false
            },
            suspend: {
                isArray: false,
                method: 'POST',
                params: {
                    action: "suspend",
                    appId: "@appId"
                }
            },
            activate: {
                isArray: false,
                method: 'POST',
                params: {
                    action: "activate",
                    appId: "@appId"
                }
            },
            reorder: {
                isArray: false,
                method: 'POST',
                params: {
                    action: "reorder"
                }
            },
            install: {
                isArray: false,
                method: 'POST',
                params: {
                    action: "install"
                }
            },
            uninstall: {
                isArray: false,
                method: 'POST',
                params: {
                    action: "uninstall",
                    appId: "@appId"
                }
            }
        });
    });

    app.service("AppStoreResource", function (urls, $resource) {
        return $resource(urls.REST_URL + 'appstore/:storeId', {
            storeId: '@id'
        }, {
            'query': {
                isArray: false
            }
        });
    });

    app.service("AppStore", function (urls, $resource) {
        function objQueryStr(obj, prefix) {
            var str = [],
                p;
            for (p in obj) {
                if (obj.hasOwnProperty(p)) {
                    var k = prefix ? prefix + "[" + p + "]" : p,
                        v = obj[p];
                    str.push((v !== null && typeof v === "object") ?
                        serialize(v, k) :
                        encodeURIComponent(k) + "=:" + encodeURIComponent(k));
                }
            }
            return str.join("&");
        }

        function AppResource(store) {
            return $resource(store.url + 'app/:storeId?server_type__name=:server_type&cartoview_version=:version', {
                storeId: '@id',
                server_type: store.server_type,
                version: versionInfo.current_version
            }, {
                'query': {
                    isArray: false,
                    method: 'JSONP',
                    params: {
                        callback: 'JSON_CALLBACK'
                    }
                }
            });
        }
        return {
            AppResource: AppResource
        }
    });


})();