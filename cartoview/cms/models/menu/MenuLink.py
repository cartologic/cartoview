from django.db import models
from django.shortcuts import redirect
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


class MenuLink(Page):
    subpage_types = []
    show_in_menus_default = True
    link_external = models.URLField("External link", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('link_external'),
    ]

    def serve(self, request, *args, **kwargs):
        return redirect(self.link_external, permanent=False)
