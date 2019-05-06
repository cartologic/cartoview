# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from wagtail.admin import messages

from .models import Server
from .tasks import harvest_task


@login_required
def harvest_resources(request, server_id):
    try:
        server = Server.objects.get(id=server_id)
    except ObjectDoesNotExist:
        messages.error(request, "Server Not Found")
    harvest_task.delay(server.id)
    index_url = "%s_%s_modeladmin_index" % (Server._meta.app_label, Server._meta.model_name)
    messages.success(request, "Server Resources Will Be Collected")
    return redirect(index_url)
