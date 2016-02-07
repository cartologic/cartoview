from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import MapConfigForm, AppInstanceForm
from cartoview.app_manager.models import *
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from geonode.maps.models import Map as GeonodeMap

class NewAppInstanceView(FormView):
    template_name = "app_manager/new_map_app_instance.html"
    form_class = AppInstanceForm
    config_form_class = MapConfigForm
    prefix = "app_instance"
    config_form_prefix = "config"
    app_name = None

    def __init__(self, **kwargs):
        super(NewAppInstanceView, self).__init__(**kwargs)
        self.instance = None

    def get_context_data(self, **kwargs):
        context = super(NewAppInstanceView,self).get_context_data(**kwargs)
        context.update(config_form=self.config_form)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.app = App.objects.get(name=self.app_name)
        geonode_map = GeonodeMap.objects.get(pk=self.request.POST.get("geonode_map_id"))
        if "config" in self.config_form.cleaned_data:
            form.instance.map_config = self.config_form.cleaned_data["config"]
        form.instance.geonode_map = geonode_map
        self.instance = form.save()
        return super(NewAppInstanceView, self).form_valid(form)

    # def form_valid(self, form):
    #     geonode_map = GeonodeMap.objects.get(pk=self.request.POST.get("geonode_map_id"))
    #     form.instance.map_config = self.config_form.cleaned_data["config"]
    #     form.instance.geonode_map = geonode_map
    #     return super(NewMapView, self).form_valid(form)

    def get_success_url(self):
        return reverse("appinstance_detail", kwargs={'appinstanceid': self.instance.pk})

    def get(self, request, *args, **kwargs):
        self.config_form = self.config_form_class(prefix=self.config_form_prefix)
        return super(NewAppInstanceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.config_form = self.config_form_class(request.POST, request.FILES, prefix=self.config_form_prefix)

        if form.is_valid() and self.config_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



def edit_app_instance(request, app_type, instance_id):
    if request.method == 'POST':
        _form = NewMapForm(request.POST, request.FILES)
        if _form.is_valid():
            new_form = _form.save(commit=False)
            new_form.app = App.objects.get(name=self.app_name)
            new_form.owner = request.user
            new_form.save()
            return HttpResponseRedirect(reverse('appinstance_detail', kwargs={'appinstanceid': new_form.pk}))
        else:
            context = {'map_form': _form, 'error': _form.errors}
    else:
        map_form = NewMapForm()
        context = {'map_form': map_form, 'oper': 'new'}
    return render_to_response(NEW_EDIT_TPL, context, context_instance=RequestContext(request))

