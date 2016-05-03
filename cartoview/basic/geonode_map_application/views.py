from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import MapConfigForm, AppInstanceForm
from cartoview.app_manager.models import *
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from geonode.maps.models import Map as GeonodeMap
from django.contrib.sites.models import Site
from django import forms

class EditAppInstanceView(FormView):
    template_name = "geonode_map_application/new_map_app_instance.html"
    form_class = AppInstanceForm
    config_form_class = MapConfigForm
    prefix = "app_instance"
    config_form_prefix = "config"
    app_name = None

    def __init__(self, **kwargs):
        super(EditAppInstanceView, self).__init__(**kwargs)
        self.instance = None

    def get_context_data(self, **kwargs):


        context = super(EditAppInstanceView, self).get_context_data(**kwargs)
        context.update(config_form=self.config_form, is_edit=self.is_edit)
        if self.app_name is not None:
            app = App.objects.get(name=self.app_name)
            context.update(app=app)
        return context

    def form_valid(self, form):
        if not self.is_edit:
            form.instance.owner = self.request.user
            form.instance.app = App.objects.get(name=self.app_name)
            geonode_map = GeonodeMap.objects.get(pk=self.request.POST.get("geonode_map_id"))
            form.instance.geonode_map = geonode_map

        if "config" in self.config_form.cleaned_data:
            form.instance.map_config = self.config_form.cleaned_data["config"]
        self.instance = form.save()
        return super(EditAppInstanceView, self).form_valid(form)

    # def form_valid(self, form):
    #     geonode_map = GeonodeMap.objects.get(pk=self.request.POST.get("geonode_map_id"))
    #     form.instance.map_config = self.config_form.cleaned_data["config"]
    #     form.instance.geonode_map = geonode_map
    #     return super(NewMapView, self).form_valid(form)

    def get_success_url(self):
        return reverse("appinstance_detail", kwargs={'appinstanceid': self.instance.pk})

    def get(self, request, *args, **kwargs):
        if issubclass(self.config_form_class, forms.ModelForm):
            self.config_form = self.config_form_class(prefix=self.config_form_prefix, instance=self.get_instance())
        else:
            self.config_form = self.config_form_class(prefix=self.config_form_prefix, initial=self.get_initial())
        return super(EditAppInstanceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.config_form = self.config_form_class(request.POST, request.FILES, prefix=self.config_form_prefix)

        if form.is_valid() and self.config_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_instance(self):
        return None

    def get_initial(self):
        if self.instance is not None:
            return {'config':self.instance.config}
        return None

    @property
    def is_edit(self):
        return self.get_instance() is not None

    def get_form_kwargs(self):
        kwargs = super(EditAppInstanceView, self).get_form_kwargs()
        kwargs.update(instance=self.get_instance())
        return kwargs
