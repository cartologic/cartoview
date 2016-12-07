/**
 * Created by kamal on 6/28/16.
 */

angular.module('cartoview.viewer.editor').service("dataService", function ($http, $tastypieResource) {

    //for post save
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
    var maps = new $tastypieResource('geonodemap', {limit: 8});
    var selected = {};
    var instanceObj = {
        config: {
            showZoombar: true,
            showLayerSwitcher: true,
            showBasemapSwitcher: true,
            showLegend: true
        }
    };
    var newInstance = true;
    if(window.instanceId){
        newInstance = false;
        var instances = new $tastypieResource('appinstances');
        instances.objects.$get({id:window.instanceId}).then(function(result){
            instanceObj.title = result.title;
            instanceObj.abstract = result.abstract;
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
        var data = "";
        data += "title=" + instanceObj.title;
        data += "&abstract=" + instanceObj.abstract;
        data += "&map=" + selected.map.id;
        data += "&config=" +  JSON.stringify(instanceObj.config);

        var promise = $http.post('', data);
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