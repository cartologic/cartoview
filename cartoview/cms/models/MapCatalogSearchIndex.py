from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.core.models import Page
from django.db.models import Q
from cartoview.maps.models import Map


class MapCatalogSearchIndex(Page):

    def get_context(self, request):
        q = request.GET.get('q', None)
        if q:
            maps = Map.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(abstract__icontains=q))
        else:
            maps = []

        # Update template context
        context = super().get_context(request)
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
