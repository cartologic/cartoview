from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class StaticPage(Page):
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/static_page/static_page_default.html', 'Default Template'),
    ), default='cms/static_page/static_page_default.html')
    hero_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.PROTECT, related_name='+', blank=True, null=True
    )
    body = RichTextField(blank=True)

    @property
    def template(self):
        return self.selected_template

    content_panels = [
        FieldPanel('title', classname="full title"),
        ImageChooserPanel('hero_image'),
        FieldPanel('body', classname="full"),
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

    class Meta:
        verbose_name = "Static Page"
