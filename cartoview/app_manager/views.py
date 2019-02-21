# from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import AppStore


class ManageAppsView(TemplateView):

    template_name = "app_manager/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stores = [store.as_dict() for store in AppStore.objects.all()]
        context.update({'stores': stores})
        return context
