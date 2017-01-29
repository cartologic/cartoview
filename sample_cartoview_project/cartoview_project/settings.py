try:
    from pre_settings import *
except:
    pass
import os
import cartoview
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cartoview_settings_path = os.path.join(os.path.dirname(cartoview.__file__), 'settings.py')
execfile(cartoview_settings_path)

MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded")
MEDIA_URL = "/uploaded/"
LOCAL_MEDIA_URL = "/uploaded/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

try:
    from local_settings import *
except:
    pass
