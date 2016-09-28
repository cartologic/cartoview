/**
 * Created by kamal on 8/11/16.
 */

angular.module('cartoview.userEngage').directive('cartoviewComments',function (urls, Comment, $rootScope) {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            identifier: "@"
        },
        template: "<div class='cv-comments'><ng-include src='templateUrl'></ng-include></div>",
        link: function (scope, element, attrs) {


            var template = attrs.template || 'default';
            scope.templateUrl = urls.STATIC_URL + "user_engage/angular-templates/comments/" + template + ".html";
            scope.comment = new Comment(scope.identifier);
            scope.onKeyPress = function(event){
                if(event.which == 13 && !event.shiftKey){
                    scope.addComment()
                }
            };
            scope.addComment = function () {
                scope.comment.addNew(scope.comment.newCommentText.trim());
                scope.comment.newCommentText = "";
            };


            // $rootScope.$watch(function(){
            //     return scope.identifier;
            // },function () {
            //     console.debug(scope.identifier);
            //     console.debug("=================================================================");
            // });
        }
    }
});

angular.module('cartoview.userEngage').directive('cartoviewImages',function (urls, Image, $mdDialog) {
    return {
        restrict: 'E',
        replace: true,
        template: "<div class='cv-images'><ng-include src='templateUrl'></ng-include></div>",
        link: function (scope, element, attrs) {
            var template = attrs.template || 'default';
            scope.templateUrl = attrs.templateUrl ||  (urls.STATIC_URL + "user_engage/angular-templates/images/" + template + ".html");

            scope.image = new Image(attrs.identifier, attrs.thumbnailSize);
            scope.image.newImageTitle = "";
            scope.onKeyPress = function(event){
                if(event.which == 13 && !event.shiftKey){
                    scope.addImage()
                }
            };
            scope.addImage = function () {
                scope.image.addNew(scope.image.newImageTitle.trim(), scope.image.imageFile[0].lfFile);
                scope.image.newImageTitle = "";
                scope.image.uploadFileApi.removeAll();
            };
            scope.showImage = function (img) {
                $mdDialog.show({
                    template: '<md-dialog class="cv-images-dialog">'
                            + '<md-dialog-content>'
                                + '<img src="' + img.image + '">'
                            + '</md-dialog-content>'
                        + '</md-dialog>',
                    parent: angular.element(document.body),
                    clickOutsideToClose:true
                });
            }
        }
    }
});



angular.module('cartoview.userEngage').directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function () {
                scope.$apply(function () {
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);