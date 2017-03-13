from geonode.groups.models import Group, GroupProfile
from cartoview.app_manager.models import App
from django.conf import settings

def news(requets):
    return {'news_app': 'cartoview_news' in settings.INSTALLED_APPS}

def apps(requets):
    return {'apps': App.objects.all().order_by('order')}
