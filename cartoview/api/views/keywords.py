from taggit.models import Tag
from cartoview.api.serializers.keywords import KeywordSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class KeywordListView(generics.ListAPIView):
    queryset = Tag.objects.all().distinct()
    serializer_class = KeywordSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
