from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.templatetags.static import static
widgets = [{
    'title': 'User Engage',
    'name': 'userEngage',
    'config': {
        'directive': '',
        'dependencies': [],
        'js': [],
        "css": []
    },
    'view': {
        'directive':
            'collector',
        'js': [
            static("vendor/angular-resource/angular-resource.min.js"),
            static("vendor/ng-image-appear/dist/ng-image-appear.min.js"),
            static(
                "vendor/lf-ng-md-file-input/dist/lf-ng-md-file-input.min.js"),
            static("user_engage/js/app.js"),
            static("user_engage/js/services.js"),
            static("user_engage/js/directives.js"),
        ],
        "css": [
            static("user_engage/css/main.css"),
            static(
                "vendor/lf-ng-md-file-input/dist/lf-ng-md-file-input.min.css"),
        ]
    },
}]
