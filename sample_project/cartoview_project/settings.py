import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
import cartoview
CARTOVIEW_ROOT = os.path.abspath(os.path.dirname(cartoview.__file__))
execfile(os.path.join(CARTOVIEW_ROOT, 'settings.py'))
ROOT_URLCONF = 'cartoview_project.urls'