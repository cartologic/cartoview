"""geonode_oauth_client URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from cartoview.api.urls import urlpatterns as api_urls
from cartoview.app_manager.urls import urlpatterns as app_manager_urls
from cartoview.geonode_oauth import views as geonode_oauth_views
from .views import IndexView
urlpatterns = i18n_patterns(
    path("django-admin/", admin.site.urls),
    re_path(r"^admin/", include(wagtailadmin_urls)),
)
urlpatterns += [
    re_path(r"^$", IndexView.as_view(), name='index'),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^accounts/profile$", geonode_oauth_views.ProfileView.as_view()),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^apps/", include(app_manager_urls)),
    re_path(r"^api/", include(api_urls)),
    re_path(r'^api-auth/', include('rest_framework.urls',
                                   namespace="rest_framework")),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    re_path(r"^sites", include(wagtail_urls), name='sites')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
