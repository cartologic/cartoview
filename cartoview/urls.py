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

from cartoview.geonode_oauth import views as geonode_oauth_views

from .views import IndexView

urlpatterns = i18n_patterns(
    path("django-admin/", admin.site.urls),
    re_path(r"^admin/", include('wagtail.admin.urls')),
)
urlpatterns += [
    re_path(r"^$", IndexView.as_view(), name='index'),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^accounts/profile$", geonode_oauth_views.ProfileView.as_view()),
    re_path(r"^documents/", include('wagtail.documents.urls')),
    re_path(r"^apps/", include('cartoview.app_manager.urls')),
    re_path(r"^api/", include('cartoview.api.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls',
                                   namespace="rest_framework")),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    re_path(r"^sites", include('wagtail.core.urls'), name='sites')
]
# django static serve static production
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
