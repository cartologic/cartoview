import os
import sys
import site

current_folder = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(current_folder, os.path.pardir))

curdir = os.path.basename(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % curdir)




from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
