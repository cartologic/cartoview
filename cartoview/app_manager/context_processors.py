from geonode.groups.models import Group, GroupProfile
from cartoview.app_manager.models import App



def apps(requets):
    return {'apps': App.objects.all().order_by('order')}
