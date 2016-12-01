from django.templatetags.static import static
widgets = [{
    'title': 'User Engage',
    'name': 'userEngage',
    'config': {
        'directive': '',
        'dependencies': [],
        'js': [


        ],
        "css": [

        ]
    },
    'view': {
        'directive': 'collector',
        'js': [
            static("vendor/angular-resource/angular-resource.min.js"),
            static("vendor/ng-image-appear/dist/ng-image-appear.min.js"),
            static("vendor/lf-ng-md-file-input/dist/lf-ng-md-file-input.min.js"),
            static("user_engage/js/app.js"),
            static("user_engage/js/services.js"),
            static("user_engage/js/directives.js"),
        ],
        "css": [
            static("user_engage/css/main.css"),
            static("vendor/lf-ng-md-file-input/dist/lf-ng-md-file-input.min.css"),
        ]
    },
}]