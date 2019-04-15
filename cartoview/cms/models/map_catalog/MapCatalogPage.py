from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Count
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from cartoview.maps.models import Map
from .MapCatalogSearchIndex import MapCatalogSearchIndex
from .MapCatalogKeywordIndex import MapCatalogKeywordIndex


class MapCatalogPage(Page):
    parent_page_types = ['HomePage']
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/map_catalog/map_catalog_page_default.html', 'Default Template'),
    ), default='cms/map_catalog/map_catalog_page_default.html')
    hero_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.PROTECT, related_name='+', blank=True, null=True
    )

    @property
    def template(self):
        return self.selected_template

    @property
    def search_url(self):
        if self.get_children().type(MapCatalogSearchIndex).count() != 0:
            return self.get_children().type(MapCatalogSearchIndex).first().url
        else:
            return None

    @property
    def keywords_url(self):
        if self.get_children().type(MapCatalogKeywordIndex).count() != 0:
            return self.get_children().type(MapCatalogKeywordIndex).first().url
        else:
            return None

    def get_context(self, request):
        context = super().get_context(request)
        keywords = Map.keywords.all()
        keywords = keywords.annotate(keywords_count=Count(Map.keywords.through.tag_relname()))
        context['keywords'] = keywords
        maps = Map.objects.all()
        paginator = Paginator(maps, 6)  # Show 6 resources per page
        page = request.GET.get('page')
        try:
            maps = paginator.page(page)
        except PageNotAnInteger:
            maps = paginator.page(1)  # If page is not an integer, deliver first page.
        except EmptyPage:
            maps = paginator.page(
                paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.
        context['maps'] = maps
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

    class Meta:
        verbose_name = "Map Catalog"
