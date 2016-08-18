/**
 * Created by kamal on 8/11/16.
 */

// angular.module('cartoview.userEngage').factory('Resource', function ($http, urls) {
//     // return $resource(urls.APPS_BASE_URL + 'rest/user_engage/image/:imageId/', {imageId: '@id'}, {
//     //     update: {
//     //         method: 'PUT'
//     //     }
//     // });
//     var getUrl = function(type) {
//         return urls.APPS_BASE_URL + 'rest/user_engage/'+ type + '/';
//     };
//
//     Resource.get = function(type, id) {
//         return $http.get(getUrl(type) + id).then(function(response) {
//             return response.data;
//         });
//     };
//
//     Resource.getAll = function(type, identifier) {
//         return $http.get(getUrl(type), {params:{identifier:identifier}}).then(function(response) {
//             return response.data.objects;
//         });
//     };
//
//     Resource.save = function(note) {
//         var url = '/api/v1/note/';
//
//         return $http.post(url, note).success(function(returnedResource) {
//             //IMPORTANT: You need to activate always_return_data in your ressource (see example)
//             note.id = returnedResource.id;
//         }).error(function(data){
//             console.log(data);
//         });
//     };
//
//     Resource.remove = function(id) {
//         return $http.delete('/api/v1/note/' + id + '/').success(function(){
//             console.log("delete successful");
//         });
//     };
//
//     return Resource;
//
//
// });


angular.module('cartoview.userEngage').factory('Comment', function ($resource, urls) {
    var CommentResource =  $resource(urls.APPS_BASE_URL + 'rest/user_engage/comment/:commentId', {identifier: '@identifier'}, {
        update: {
            method: 'PUT'
        }
    });
    var Comment = function (identifier) {
        var self = this;
        self.identifier = identifier;
        self.list = {};
        this.loadAll = function () {
            CommentResource.get({identifier:this.identifier}).$promise.then(function (res) {
                self.list =  res;
            });
        };
        this.addNew = function (comment) {
            self.saving = true;
            new CommentResource({
                comment: comment,
                identifier: this.identifier
            }).$save(function (newComment) {
                self.saving = false;
                self.loadAll();
            }, this);
        };
        this.loadAll();
    };
    return Comment
});

angular.module('cartoview.userEngage').factory('Image', function ($resource, urls, $http) {
    var url = urls.APPS_BASE_URL + 'rest/user_engage/image/';
    var ImageResource =  $resource(url + ':imageId', {
        identifier: '@identifier',
        thumbnailSize: "@thumbnailSize"
    }, {
        update: {
            method: 'PUT'
        }
    });
    var Image = function (identifier, thumbnailSize) {
        var self = this;
        self.identifier = identifier;
        self.thumbnailSize = thumbnailSize || "256,256";
        self.list = {};
        this.loadAll = function () {
            ImageResource.get({
                identifier: this.identifier,
                thumbnailSize: this.thumbnailSize
            }).$promise.then(function (res) {
                self.list =  res;
            });
        };
        this.addNew = function (title, imageFile) {
            self.saving = true;

            var fd = new FormData();
            fd.append('image', imageFile, imageFile.name);
            fd.append('identifier', this.identifier);
            fd.append('title', title);
            $http.post(url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).then(function (res) {
                console.debug(res);
                self.saving = false;
                self.loadAll();
            });
            // new ImageResource({
            //     title: title,
            //     image:image,
            //     identifier: this.identifier
            // }).$save(function (newImage) {
            //     self.saving = false;
            //     self.loadAll();
            // }, this);
        };
        this.loadAll();
    };
    return Image
});
