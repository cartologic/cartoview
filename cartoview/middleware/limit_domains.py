from django.contrib.sites.models import Site
from django.http import Http404


class LimitDomainsMiddleware(object):
    def process_response(self, request, response):
        host = request.META['HTTP_HOST']
        # if Site.objects.filter(domain=host).count() == 0:
        #     raise Http404("%s is not found!" % host)
        return response
