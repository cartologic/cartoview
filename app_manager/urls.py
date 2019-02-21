from django.urls import re_path
from .views import ManageAppsView
app_name = 'app_manager'
urlpatterns = ([
    re_path('manage', ManageAppsView.as_view(), name='manage-apps'),
], 'app_manager')
