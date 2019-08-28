from django.http import HttpResponseRedirect

from wagtail.core.models import Page


class LanguageRedirectionPage(Page):

    def serve(self, request):
        return HttpResponseRedirect(request.site.root_url + '/' + self.title + '/home')
