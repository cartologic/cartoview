/**
 * Created by kamal on 8/11/16.
 */

angular.module('cartoview.userEngage').directive('cartoviewComments', function (urls, Comment, $rootScope, cartoviewUser) {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            identifier: "@"
        },
        template: "<div class='cv-comments'><ng-include src='templateUrl'></ng-include></div>",
        link: function (scope, element, attrs) {


            var template = attrs.template || 'default';
            scope.authenticated = cartoviewUser.isAuthenticated;
            scope.templateUrl = urls.STATIC_URL + "user_engage/angular-templates/comments/" + template + ".html";
            scope.comment = new Comment(scope.identifier);
            scope.onKeyPress = function (event) {
                if (event.which == 13 && !event.shiftKey) {
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

angular.module('cartoview.userEngage').directive('cartoviewImages', function (urls, Image, $mdDialog, cartoviewUser) {
    return {
        restrict: 'E',
        replace: true,
        template: "<div class='cv-images'><ng-include src='templateUrl'></ng-include></div>",
        link: function (scope, element, attrs) {
            var template = attrs.template || 'default';
            scope.templateUrl = attrs.templateUrl || (urls.STATIC_URL + "user_engage/angular-templates/images/" + template + ".html");
            scope.authenticated = cartoviewUser.isAuthenticated;
            scope.image = new Image(attrs.identifier, attrs.thumbnailSize);
            scope.image.newImageTitle = "";
            scope.onKeyPress = function (event) {
                if (event.which == 13 && !event.shiftKey) {
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
                    clickOutsideToClose: true
                });
            }
            scope.showUploadImage = function (ev) {
                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: urls.STATIC_URL + 'user_engage/angular-templates/images/images.dialog.tpl.html',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                    locals: {parentScope: scope},
                    fullscreen: false
                });
            };
            function DialogController($scope, parentScope) {
                $scope.parent = parentScope;
                $scope.cancel = function () {
                    $mdDialog.cancel();
                };
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
// angular.module('cartoview.userEngage').directive('slideThumb', function (urls, $timeout) {
//     return {
//         restrict: 'E',
//         templateUrl: urls.STATIC_URL + "user_engage/angular-templates/images/slider_thumb.tmp.html",
//         link: function (scope, element, attrs) {
//             scope.images = attrs.images;
//             console.log(attrs.images)
//             $timeout(function () {
//                   var options = {
//                       $AutoPlay: 0,                                   //[Optional] Auto play or not, to enable slideshow, this option must be set to greater than 0. Default value is 0. 0: no auto play, 1: continuously, 2: stop at last slide, 4: stop on click, 8: stop on user navigation (by arrow/bullet/thumbnail/drag/arrow key navigation)
//                       $SlideDuration: 500,                                //[Optional] Specifies default duration (swipe) for slide in milliseconds, default value is 500
//
//                       $ThumbnailNavigatorOptions: {                       //[Optional] Options to specify and enable thumbnail navigator or not
//                           $Class: $JssorThumbnailNavigator$,              //[Required] Class to create thumbnail navigator instance
//                           $ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
//
//                           $ActionMode: 1,                                 //[Optional] 0 None, 1 act by click, 2 act by mouse hover, 3 both, default value is 1
//                           $SpacingX: 8,                                   //[Optional] Horizontal space between each thumbnail in pixel, default value is 0
//                           $Cols: 10,                             //[Optional] Number of pieces to display, default value is 1
//                           $ParkingPosition: 360                           //[Optional] The offset position to park thumbnail
//                       }
//                   };
//
//             var jssor_slider1 = new $JssorSlider$('slider1_container', options);
//             }, 1000)
//
//
//         }
//     };
// });