from cartoview.app_manager.models import App, AppInstance, Logo
from django.conf import settings


def news(request):
    return {'news_app': 'cartoview_news' in settings.INSTALLED_APPS}


def apps(request):
    return {'apps': App.objects.all().order_by('order')}


def apps_menu(request):
    return {'APPS_MENU': settings.APPS_MENU}


def workspace(request):
    return {'WORKSPACE_ENABLED': settings.WORKSPACE_ENABLED}


def apps_instance(request):
    instances = AppInstance.objects.all()
    num = AppInstance.objects.all().count()
    return {'apps_instance_count': num, 'instances': instances.order_by('app__order')[:5]}


from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404


def site_logo(request):
    try:
        logo = get_object_or_404(Logo, site=Site.objects.get_current())
        return {'site_logo': logo}
    except:
        return {'site_logo': None}
