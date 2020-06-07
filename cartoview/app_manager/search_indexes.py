from pinax.ratings.models import OverallRating
from dialogos.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models import Avg
from haystack import indexes

from .models import AppInstance


class AppInstanceIndex(indexes.SearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='resourcebase_ptr_id')
    abstract = indexes.CharField(model_attr="abstract", boost=1.5)
    category__gn_description = indexes.CharField(
        model_attr="category__gn_description", null=True)
    csw_type = indexes.CharField(model_attr="csw_type")
    csw_wkt_geometry = indexes.CharField(model_attr="csw_wkt_geometry")
    detail_url = indexes.CharField(model_attr="get_absolute_url")
    owner__username = indexes.CharField(
        model_attr="owner", faceted=True, null=True)
    popular_count = indexes.IntegerField(
        model_attr="popular_count",
        default=0,
        boost=20)
    share_count = indexes.IntegerField(model_attr="share_count", default=0)
    rating = indexes.IntegerField(null=True)
    supplemental_information = indexes.CharField(
        model_attr="supplemental_information", null=True)
    thumbnail_url = indexes.CharField(model_attr="thumbnail_url", null=True)
    uuid = indexes.CharField(model_attr="uuid")
    title = indexes.CharField(model_attr="title", boost=2)
    date = indexes.DateTimeField(model_attr="date")

    text = indexes.EdgeNgramField(
        document=True, use_template=True, stored=False)
    type = indexes.CharField(faceted=True)
    title_sortable = indexes.CharField(
        indexed=False, stored=False)  # Necessary for sorting
    category = indexes.CharField(
        model_attr="category__identifier",
        faceted=True,
        null=True,
        stored=True)
    keywords = indexes.MultiValueField(
        model_attr="keyword_slug_list",
        null=True,
        faceted=True,
        stored=True)
    regions = indexes.MultiValueField(
        model_attr="region_name_list",
        null=True,
        faceted=True,
        stored=True)
    popular_count = indexes.IntegerField(
        model_attr="popular_count",
        default=0,
        boost=20)
    share_count = indexes.IntegerField(model_attr="share_count", default=0)
    rating = indexes.IntegerField(null=True)
    num_ratings = indexes.IntegerField(stored=False)
    num_comments = indexes.IntegerField(stored=False)
    app__name = indexes.CharField(faceted=False, null=True)
    app__title = indexes.CharField(faceted=False, null=True)
    launch_app_url = indexes.CharField(faceted=False, null=True)
    edit_url = indexes.CharField(faceted=False, null=True)

    def get_model(self):
        return AppInstance

    def prepare_type(self, obj):
        return "appinstance"

    def prepare_app__name(self, obj):
        return obj.app.name

    def prepare_app__title(self, obj):
        return obj.app.title

    def prepare_launch_app_url(self, obj):
        if obj.app is not None:
            return reverse(
                "%s.view" % obj.app.name, args=[obj.pk])
        return None

    def prepare_edit_url(self, obj):
        if obj.app is not None:
            return reverse(
                "%s.edit" % obj.app.name, args=[obj.pk])
        return None

    def prepare_rating(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        try:
            rating = OverallRating.objects.filter(
                object_id=obj.pk,
                content_type=ct
            ).aggregate(r=Avg("rating"))["r"]
            return float(str(rating or "0"))
        except OverallRating.DoesNotExist:
            return 0.0

    def prepare_num_ratings(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        try:
            return OverallRating.objects.filter(
                object_id=obj.pk,
                content_type=ct
            ).all().count()
        except OverallRating.DoesNotExist:
            return 0

    def prepare_num_comments(self, obj):
        try:
            return Comment.objects.filter(
                object_id=obj.pk,
                content_type=ContentType.objects.get_for_model(obj)
            ).all().count()
        except BaseException:
            return 0

    def prepare_title_sortable(self, obj):
        return obj.title.lower()
