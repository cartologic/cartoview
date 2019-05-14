from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, TabbedInterface, ObjectList
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from .grid.GridBlock import GridBlock
from .blocks.Blocks import HeroAreaBlock, MapCatalogBlock
from .blocks.ThumbnailGalleryBlock import ThumbnailGalleryBlock
from .blocks.ImageTextOverlayBlock import ImageTextOverlayBlock


class HomePage(Page):
    parent_page_types = ['wagtailcore.Page']
    hero = StreamField([
        ('hero_area', HeroAreaBlock()),
    ], blank=True, null=True, help_text=mark_safe("You should add only <b>1 Hero</b>"))
    body = StreamField([
        ('map_catalog', MapCatalogBlock()),
        ('grid', GridBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
    ], blank=True, null=True)
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/home_page_default.html', 'Default Template'),
    ), default='cms/home_page_default.html')

    @property
    def template(self):
        return self.selected_template

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel("hero", classname="Full"),
        StreamFieldPanel("body", classname="Full"),
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
        verbose_name = "Site Homepage"
