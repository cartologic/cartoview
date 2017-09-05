from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from account.decorators import login_required
from django.shortcuts import render
from cartoview.app_manager.models import AppInstance
from geonode.documents.models import Document
from geonode.groups.models import GroupProfile
from geonode.layers.models import Layer
from geonode.maps.models import Map


@login_required
def workspace(request):
    owner = request.user
    apps = AppInstance.objects.filter(owner=owner)
    created_apps = AppInstance.objects.all()
    layers = Layer.objects.filter(owner=owner)
    maps = Map.objects.filter(owner=owner)
    maps_count = Map.objects.all().count()
    layers_count = Layer.objects.all().count()
    documents = Document.objects.filter(owner=owner)
    documents_count = Document.objects.all().count()
    groups = owner.group_list_all()
    groups_count = GroupProfile.objects.all().count()
    return render(
        request,
        template_name='workspace/workspace.html',
        context={
            'my_apps': apps,
            'my_layers': layers,
            'created_apps': created_apps,
            'my_maps': maps,
            'maps_count': maps_count,
            'layers_count': layers_count,
            "groups": groups,
            "groups_count": groups_count,
            "documents": documents,
            "documents_count": documents_count
        })
