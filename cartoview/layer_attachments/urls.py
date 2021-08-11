from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import AttachmentViewSet, LayerViewSet, DownloadAttachmentsView, view

router = routers.DefaultRouter()
router.register(r'layers', LayerViewSet, basename="layers")
router.register(r'attachments', AttachmentViewSet, basename="attachments")

urlpatterns = [
    path('layer_attachments/', view, name="layer_attachments"),
    path('api/layer_attachments/', include(router.urls)),
    path('api/layer_attachments/download/', DownloadAttachmentsView.as_view())
]
