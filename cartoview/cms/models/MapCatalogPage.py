from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class MapCatalogPage(Page):
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/map_catalog_page_default.html', 'Default Template'),
    ), default='cms/map_catalog_page_default.html')
    hero_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.PROTECT, related_name='+', blank=True, null=True
    )

    @property
    def template(self):
        return self.selected_template

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')

        # Update template context
        context = super().get_context(request)
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        ImageChooserPanel('hero_image'),
    ]

    theme_panels = [
        FieldPanel('selected_template', widget=forms.Select),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
