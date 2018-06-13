/**
 * @license Angular Resource Tastypie v1.0.5
 * (c) 2014-2016 Marcos William Ferretti, https://github.com/mw-ferretti/angular-resource-tastypie
 * License: MIT
 */

var ngResourceTastypie = {
    name: 'Angular Resource Tastypie',
    description: 'RESTful AngularJs client for Django-Tastypie or equivalent schema.',
    version: {
        full: '1.0.5',
        major: 1,
        minor: 0,
        dot: 5,
        codeName: 'Cappuccino'
    },
    author: {
        name: 'Marcos William Ferretti',
        email: 'ferretti.spo@gmail.com',
        github: 'https://github.com/mw-ferretti/',
        linkedin: 'https://www.linkedin.com/in/mwferretti'
    },
    license: 'MIT, (c) 2014-2016 Marcos William Ferretti',
    source: 'https://github.com/mw-ferretti/angular-resource-tastypie'
};

if(typeof angular == 'undefined')
    throw '[ngResourceTastypie v'.concat(ngResourceTastypie.version.full,'] Requires AngularJs 1.3+');

if(angular.version.major < 1 || (angular.version.major == 1 && angular.version.minor < 3))
    throw '[ngResourceTastypie v'.concat(ngResourceTastypie.version.full,'] Requires AngularJs 1.3+, your version is ', angular.version.full);


angular.module('ngResourceTastypie', ['ngResource'])
.constant('ngResourceTastypie', ngResourceTastypie)

.config(['$resourceProvider', function($resourceProvider){
    $resourceProvider.defaults.stripTrailingSlashes = false;
}])

.provider('$tastypie', ['$httpProvider', function($httpProvider){

    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $httpProvider.defaults.headers.common['Content-Type'] = 'application/json';

    var self = this;
    var resource_url = '';
    var resource_domain = '';

    var auth = {
        username : '',
        api_key : ''
    };

    self.providers = {};
    self.default = {};

    self.getProvider = function(providerName){
        var provider = {};
        if(providerName == 'default'){
            provider = self.default || {};
        }else{
            provider = self.providers[providerName] || {};
        }
        if(!provider.hasOwnProperty('url')){
            throw '[$tastypieProvider][GetProvider] provider "'.concat(providerName,'" not found.');
        }
        return provider;
    };

    self.setDefault = function(providerName){
        if(!self.providers.hasOwnProperty(providerName)){
            throw '[$tastypieProvider][ProviderSetDefault] Provider '.concat(providerName, ' not found.');
        }
        self.default = self.providers[providerName];
        resource_url = self.default['url'];
        resource_domain = self.default['domain'];
        auth.username = self.default['username'];
        auth.api_key = self.default['apikey'];

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieDefaultProvider = angular.toJson(self.default);
        }
    };

    self.add = function(providerName, providerObj){
        var validProviderName = (providerName && (typeof(providerName) === 'string' || providerName instanceof String));
        if(!validProviderName){
            throw '[$tastypieProvider][ProviderAdd] Invalid providerName string. Usage: add("providerName", {url:"address"})';
        }
        if(!providerObj || !angular.isObject(providerObj) || !providerObj.hasOwnProperty('url')){
            throw '[$tastypieProvider][ProviderAdd] Invalid providerObj object. Usage: add("providerName", {url:"address"})';
        }
        if(self.providers[providerName]){
            return self;
        }

        providerObj.name = providerName;

        var el_href  = document.createElement('a');
        el_href.href = providerObj.url;
        var domain = el_href.protocol.concat('//', el_href.hostname);
        if (el_href.port != '') domain = domain.concat(':', el_href.port);
        providerObj.domain = domain;

        if(!providerObj.hasOwnProperty('headers')){
            providerObj.headers = {};
        }

        if(!providerObj.headers.hasOwnProperty('Content-Type')){
            providerObj.headers['Content-Type'] = 'application/json';
        }

        if(providerObj.hasOwnProperty('username') && providerObj.hasOwnProperty('apikey')){
            providerObj.headers.Authorization = 'ApiKey '.concat(
                providerObj.username, ':', providerObj.apikey
            );
        }

        self.providers[providerName] = providerObj;

        if(!self.default.hasOwnProperty('name')){
            self.setDefault(providerName);
        }

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieProviders = angular.toJson(self.providers);
        }

        return self;
    };

    self.httpExceptions = {};
    self.httpExceptionsAdd = function(httpCode, callback){
        if(!httpCode){
            throw '[$tastypieProvider][httpExceptionsAdd] Invalid httpCode integer. Usage: httpExceptionsAdd(httpCode, callback)';
        }
        if(!callback || !angular.isFunction(callback)){
            throw '[$tastypieProvider][httpExceptionsAdd] Invalid callback function. Usage: httpExceptionsAdd(httpCode, callback)';
        }
        self.httpExceptions['c'.concat(httpCode)] = callback;
        return self;
    };

    self.setProviderAuth = function(providerName, username, apikey){
        var providerObj = self.getProvider(providerName);
        providerObj.username = username;
        providerObj.apikey = apikey;

        if(!providerObj.hasOwnProperty('headers')){
            providerObj.headers = {};
        }

        providerObj.headers.Authorization = 'ApiKey '.concat(
            providerObj.username, ':', providerObj.apikey
        );

        self.providers[providerName] = providerObj;

        if(self.default.name == providerName){
            self.default = providerObj;
            if(typeof(Storage) !== "undefined"){
                sessionStorage.$tastypieDefaultProvider = angular.toJson(self.default);
            }
        }

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieProviders = angular.toJson(self.providers);
        }
    };

    self.setResourceUrl = function(url){
        var validUrl = (url && (typeof(url) === 'string' || url instanceof String));
        if(!validUrl){
            throw '[$tastypieProvider][SetResourceUrl] Invalid URL.';
        }

        resource_url = url;

        var dominio  = document.createElement('a');
        dominio.href = resource_url;
        resource_domain = dominio.protocol.concat('//', dominio.hostname);
        if (dominio.port != '') resource_domain = resource_domain.concat(':', dominio.port);

        self.default.name = 'default';
        if(!self.default.hasOwnProperty('headers')){
            self.default.headers = {};
        }
        if(!self.default.headers.hasOwnProperty('Content-Type')){
            self.default.headers['Content-Type'] = 'application/json';
        }
        self.default.url = url;
        self.default.domain = resource_domain;

        self.providers[self.default.name] = self.default;

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieDefaultProvider = angular.toJson(self.default);
            sessionStorage.$tastypieProviders = angular.toJson(self.providers);
        }
    };

    self.setAuth = function(username, apikey){
        var validUsername = (username && (typeof(username) === 'string' || username instanceof String));
        var validApikey = (apikey && (typeof(apikey) === 'string' || apikey instanceof String));
        if(!validUsername){
            throw '[$tastypieProvider][SetResourceUrl] Invalid username.';
        }
        if(!apikey){
            throw '[$tastypieProvider][SetResourceUrl] Invalid apikey.';
        }

        auth.username = username;
        auth.api_key = apikey;

        self.default.name = 'default';
        if(!self.default.hasOwnProperty('headers')){
            self.default.headers = {};
        }
        if(!self.default.headers.hasOwnProperty('Content-Type')){
            self.default.headers['Content-Type'] = 'application/json';
        }

        self.default.username = username;
        self.default.apikey = apikey;
        self.default.headers.Authorization = 'ApiKey '.concat(username, ':', apikey);

        self.providers[self.default.name] = self.default;

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieDefaultProvider = angular.toJson(self.default);
            sessionStorage.$tastypieProviders = angular.toJson(self.providers);
        }
    };

    var clearAuthSessionAux = function(providerObj){
        if(!angular.isObject(providerObj) || !providerObj.hasOwnProperty('url')){
            throw '[$tastypieProvider][clearAuthProvider] Invalid provider.';
        }

        if(providerObj.hasOwnProperty('username')){
            providerObj.username = '';
        }

        if(providerObj.hasOwnProperty('apikey')){
            providerObj.apikey = '';
        }

        if(providerObj.hasOwnProperty('headers')){
            if(providerObj.headers.hasOwnProperty('Authorization')){
                delete providerObj.headers["Authorization"];
            }
        }

        self.providers[providerObj.name] = providerObj;

        if(typeof(Storage) !== "undefined"){
            sessionStorage.$tastypieProviders = angular.toJson(self.providers);
        }

        if(providerObj.name == self.default.name){
            auth.username = '';
            auth.api_key = '';
            self.default = providerObj;
            if(typeof(Storage) !== "undefined"){
                sessionStorage.$tastypieDefaultProvider = angular.toJson(self.default);
            }
        }
    };

    self.clearAuthSession = function(providerName){
        var validProviderName = (providerName && (typeof(providerName) === 'string' || providerName instanceof String));

        if(!validProviderName){
            throw '[$tastypieProvider][ClearAuthSession] Invalid providerName.';
        }

        if(providerName == 'all'){
            var providerList = Object.keys(self.providers);
            for(var i=0; i<providerList.length; i++){
                clearAuthSessionAux(self.providers[providerList[i]]);
            }
        }else{
            clearAuthSessionAux(self.getProvider(providerName));
        }
    };

    self.close = function(){
        self.clearAuthSession('all');
    };

    self.getAuth = function(){
        return auth;
    };

    self.getResourceUrl = function(){
        return resource_url;
    };

    self.getResourceDomain = function(){
        return resource_domain;
    };

    if(typeof(Storage) !== "undefined"){
        self.default = angular.fromJson(sessionStorage.$tastypieDefaultProvider) || {};
        self.providers = angular.fromJson(sessionStorage.$tastypieProviders) || {};
        resource_url = self.default['url'];
        resource_domain = self.default['domain'];
        auth.username = self.default['username'];
        auth.api_key = self.default['apikey'];
    }

    var working_list = [];
    Object.defineProperties(self, {
        "working": {
            "get": function(){
                return (working_list.length > 0);
            },
            "set": function(b){
                if(typeof(b) == 'undefined') b = false;
                if(b) working_list.push(1);
                else working_list.splice(-1,1);
            }
        }
    });

    self.$get = function(){
        return {
            providers:self.providers,
            add:self.add,
            getProvider:self.getProvider,
            setDefault:self.setDefault,
            setProviderAuth:self.setProviderAuth,
            default:self.default,
            clearAuthSession:self.clearAuthSession,
            resource_url:self.getResourceUrl(),
            resource_domain:self.getResourceDomain(),
            auth:self.getAuth(),
            working:self.working,
            setAuth:self.setAuth,
            setResourceUrl:self.setResourceUrl,
            close:self.close,
            httpExceptionsAdd:self.httpExceptionsAdd,
            httpExceptions:self.httpExceptions
        }
    };
}])

.factory('$tastypiePaginator', ['$resource', '$tastypie', '$q', function($resource, $tastypie, $q){

    function $tastypiePaginator(tastypieResource, filters, result){

        this.resource = tastypieResource;
        this.filters = filters || {};
        this.meta = {};
        this.objects = [];
        this.index = 0;
        this.length = 0;
        this.range = [];

        setPage(this, result);
    }

    function promise_except_data_invalid(msg){
        var deferred = $q.defer();
        if (typeof(console) == "object") console.log(msg);
        deferred.reject({statusText:msg});
        return deferred.promise;
    }

    function setPage(self, result){
        if (!angular.isObject(result.meta)) throw '[$tastypiePaginator] Invalid django-tastypie object.';

        self.meta = result.meta;

        for (var x=0; x<result.objects.length; x++){
            result.objects[x] = self.resource.objects.$create(result.objects[x]);
        }

        self.objects = result.objects;
        self.length = Math.ceil(result.meta.total_count / (result.meta.limit || 1));

        if (result.meta.offset == 0) self.index = 1;
        else self.index = (Math.ceil(result.meta.offset / (result.meta.limit || 1))+1);

        var pgs = [];
        for (var i=1;i<=self.length;i++) {pgs.push(i);}
        self.range = pgs;
    }

    function getPage(self, end_url){
        if (end_url){
            self.resource.working = true;
            var promise = $resource(end_url, {}, {
                'get':{
                    method:'GET',
                    headers: self.resource.provider.headers
                }
            }).get().$promise.then(
                function(result){
                    setPage(self, result);
                    self.resource.working = false;
                    return self;
                },
                function(error){
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    error = error || {};
                    error.statusText = '[$tastypiePaginator][$get] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        }else{
            var msg = '[$tastypiePaginator][$get] '.concat('Invalid url.');
            return promise_except_data_invalid(msg);
        }
    }

    function changePage(self, index, update){
        if((index == self.index) && (!update)){
            var msg = '[$tastypiePaginator][$get] '.concat('Index ', index, ' has already been loaded.');
            return promise_except_data_invalid(msg);
        }

        if ((index > 0) && (index <= self.length)){
            self.resource.working = true;
            var filters = angular.copy(self.filters);
            filters.offset = ((index-1)*self.meta.limit);

            var promise = $resource(self.resource.endpoint, self.resource.defaults, {
                'get':{
                    method:'GET',
                    headers: self.resource.provider.headers
                }
            }).get(filters).$promise.then(
                function(result){
                    if(result.meta.offset == result.meta.total_count){
                        if((index - 1) == 0){
                            setPage(self, result);
                            self.resource.working = false;
                            return self;
                        }else{
                            self.resource.working = false;
                            return changePage(self, (index - 1), true);
                        }
                    }else{
                        setPage(self, result);
                        self.resource.working = false;
                        return self;
                    }
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypiePaginator][$get] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        }else{
            var msg = '[$tastypiePaginator][$get] '.concat('Index ', index, ' not exist.');
            return promise_except_data_invalid(msg);
        }
    }

    $tastypiePaginator.prototype.change = function(index){
        if (index)
            return changePage(this,index,false);
        else{
            var msg = '[$tastypiePaginator][change] '.concat('Parameter "index" not informed.');
            return promise_except_data_invalid(msg);
        }
    };

    $tastypiePaginator.prototype.next = function(){
        if (this.meta.next)
            return getPage(this, $tastypie.resource_domain.concat(this.meta.next));
        else{
            var msg = '[$tastypiePaginator][next] '.concat('Not exist next pages.');
            return promise_except_data_invalid(msg);
        }
    };

    $tastypiePaginator.prototype.previous = function(){
        if (this.meta.previous)
            return getPage(this, $tastypie.resource_domain.concat(this.meta.previous));
        else{
            var msg = '[$tastypiePaginator][previous] '.concat('Not exist previous pages.');
            return promise_except_data_invalid(msg);
        }
    };

    $tastypiePaginator.prototype.refresh = function(){
        return changePage(this,this.index,true);
    };

    $tastypiePaginator.prototype.first = function(){
        return changePage(this,1,false);
    };

    $tastypiePaginator.prototype.last = function(){
        return changePage(this,this.length,false);
    };

    return $tastypiePaginator;
}])


.factory('$tastypieObjects', ['$resource', '$tastypiePaginator', '$q', '$tastypie', function($resource, $tastypiePaginator, $q, $tastypie){

    function $tastypieObjects(tastypieResource){
        this.resource = tastypieResource;
    }

    function promise_except_data_invalid(msg){
        var deferred = $q.defer();
        if (typeof(console) == "object") console.log(msg);
        deferred.reject({statusText:msg});
        return deferred.promise;
    }

    function create(self, data){

        var custom_method = {
            'post':{
                method:'POST',
                headers: self.resource.provider.headers
            },
            'save':{
                method:'POST',
                headers: self.resource.provider.headers
            },
            'get':{
                method:'GET',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'get_uri':{
                method:'GET',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'update':{
                method:'PATCH',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'put':{
                method:'PUT',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'patch':{
                method:'PATCH',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'delete':{
                method:'DELETE',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            },
            'remove':{
                method:'DELETE',
                headers: self.resource.provider.headers,
                url:self.resource.endpoint.concat(":id/")
            }
        };

        var obj = $resource(self.resource.endpoint, {id:'@id'}, custom_method);
        delete obj.prototype['$query'];
        obj.prototype.$domain = self.resource.provider.domain;
        obj.prototype.$get = function(data){
            var fields = this;
            angular.extend(fields, (data || {}));

            if(!fields.hasOwnProperty('id')){
                var msg = '[$tastypieObjects][$get] '.concat('Attribute [id] is required.');
                return promise_except_data_invalid(msg);
            }

            self.resource.working = true;
            var promise = fields.$get_uri(fields).then(
                function(result){
                    self.resource.working = false;
                    return result;
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypieObjects][$get] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        };

        obj.prototype.$save = function(data){
            var fields = this;
            angular.extend(fields, (data || {}));
            var ws = fields.hasOwnProperty('id') ? fields.$put() : fields.$post();

            self.resource.working = true;
            var promise = ws.then(
                function(result){
                    self.resource.working = false;
                    if (typeof(self.resource.page.refresh) == typeof(Function))
                        self.resource.page.refresh();
                    return result;
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypieObjects][$save] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        };

        obj.prototype.$update = function(data){
            var fields = this;
            angular.extend(fields, (data || {}));

            if(!fields.hasOwnProperty('id') || !fields.id){
                var msg = '[$tastypieObjects][$update] '.concat('Attribute [id] is required.');
                return promise_except_data_invalid(msg);
            }

            self.resource.working = true;
            var promise = fields.$patch().then(
                function(result){
                    self.resource.working = false;
                    if (typeof(self.resource.page.refresh) == typeof(Function))
                        self.resource.page.refresh();
                    return result;
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypieObjects][$update] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        };

        obj.prototype.$delete = function(data){
            var fields = this;
            angular.extend(fields, (data || {}));

            if(!fields.hasOwnProperty('id') || !fields.id){
                var msg = '[$tastypieObjects][$delete] '.concat('Attribute [id] is required.');
                return promise_except_data_invalid(msg);
            }

            self.resource.working = true;
            var promise = fields.$remove().then(
                function(result){
                    self.resource.working = false;
                    angular.forEach(fields, function(value, key){delete fields[key]});
                    if (typeof(self.resource.page.refresh) == typeof(Function))
                            self.resource.page.refresh();
                    return result;
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypieObjects][$delete] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        };

        obj.prototype.$clear = function(){
            var fields = this;
            angular.forEach(fields, function(value, key){delete fields[key]});
        };

        return new obj(data);
    };

    function find(self){

        var obj = $resource(self.resource.endpoint, self.resource.defaults, {
            'get':{method:'GET', headers: self.resource.provider.headers},
            'find':{method:'GET', headers: self.resource.provider.headers}
        });

        obj.prototype.$find = function(filter){
            self.resource.working = true;
            var promise = this.$get(filter).then(
                function(result){
                    self.resource.working = false;
                    self.resource.page = new $tastypiePaginator(self.resource, filter, result);
                    return self.resource.page;
                },
                function(error){
                    error = error || {};
                    error.statusText = '[$tastypieObjects][$find] '.concat(error.statusText || 'Server Not Responding.');
                    self.resource.working = false;
                    var fn = $tastypie.httpExceptions['c'.concat(error.status)];
                    if(fn && angular.isFunction(fn)){
                        fn(error);
                    }
                    throw error;
                }
            );
            return promise;
        };

        return new obj();
    }

    $tastypieObjects.prototype.$create = function(data){
        return create(this, data);
    };

    $tastypieObjects.prototype.$get = function(data){
        return create(this).$get(data);
    };

    $tastypieObjects.prototype.$delete = function(data){
        return create(this, data).$delete();
    };

    $tastypieObjects.prototype.$find = function(data){
        return find(this).$find(data);
    };

    $tastypieObjects.prototype.$update = function(data){
        return create(this, data).$update();
    };

    return $tastypieObjects;
}])

.factory('$tastypieResource', ['$resource', '$tastypie', '$tastypiePaginator', '$tastypieObjects', function($resource, $tastypie, $tastypiePaginator, $tastypieObjects){

        function $tastypieResource(service, default_filters, provider_name) {

            var validService = (service && (typeof(service) === 'string' || service instanceof String));

            if (!validService){
                throw '[$tastypieResource] Unknown service name.';
            }

            this.provider = $tastypie.getProvider(provider_name || 'default');
            this.endpoint = this.provider.url.concat(service, '/');
            this.defaults = default_filters || {};
            this.page = {};
            this.objects = new $tastypieObjects(this);

            var working_list = [];
            Object.defineProperties(this, {
                "working": {
                    "get": function(){
                        return (working_list.length > 0);
                    },
                    "set": function(b){
                        if(typeof(b) == 'undefined') b = false;
                        if(b) working_list.push(1);
                        else working_list.splice(-1,1);
                        $tastypie.working = b;
                    }
                }
            });
        }

        return $tastypieResource;
}]);
