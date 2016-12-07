/**
 * Created by kamal on 6/28/16.
 */
'use strict';
(function () {
    window.angularAppDependencies = window.angularAppDependencies || [];
    console.debug(window.angularAppDependencies)
    var module = angular.module('cartoview.viewer.editor', [
        'cartoview.base',
        'ngResourceTastypie',
        'cartoview.viewer.widgetsInfo',
        'cartoview.viewer.urlsHelper'
    ].concat(window.angularAppDependencies));
    module.config(function($tastypieProvider, $httpProvider, urlsHelper){
        $tastypieProvider.setResourceUrl(urlsHelper.rest);

        $tastypieProvider.add('geonode', {url: urlsHelper.geonodeRest});
        //$tastypieProvider.setDefault('cartoview');

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
})();