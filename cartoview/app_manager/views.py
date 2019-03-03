# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import TemplateView


class ManageAppsView(TemplateView):

    template_name = "app_manager/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def plugins_view(request):
    return render(request, 'app_manager/wagtail_app_manager.html')
