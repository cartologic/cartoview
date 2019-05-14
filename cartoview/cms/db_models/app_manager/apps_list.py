from cartoview.app_manager.models import App
from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class AppChooserblock(blocks.ChooserBlock):
    target_model = App
    widget = forms.Select

    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        else:
            return value


class AppsPage(Page):
    heading = models.CharField(max_length=255, blank=False, null=False, default="Apps")
    abstract = models.TextField(blank=True, null=True)
    apps = StreamField(
        [('apps', AppChooserblock(required=True),)], blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('abstract', classname="full"),
        StreamFieldPanel('apps'),
    ]
    @property
    def apps_list(self):
        apps = [app.value for app in self.apps]
        if len(apps) == 0:
            apps = App.objects.all()
        return apps

    def get_context(self, request):
        context = super().get_context(request)
        return context
