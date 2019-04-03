from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from fernet_fields import EncryptedTextField
from guardian.shortcuts import assign_perm

from cartoview.log_handler import get_logger

from . import SUPPORTED_SERVERS
from .utils import get_handler_class_handler

logger = get_logger(__name__)
CONNECTION_PERMISSIONS = (
    ("use_for_read", _("Allow to use for read operations")),
    ("use_for_write", _("Allow to use for write operations")),
)


class BaseConnectionModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ('-created_at', '-updated_at')

    def to_dict(self):
        return model_to_dict(self)


class Server(BaseConnectionModel):
    SERVER_TYPES = [(s.value, s.title) for s in SUPPORTED_SERVERS]
    server_type = models.CharField(
        max_length=15, choices=SERVER_TYPES, help_text=_("Server Type"))
    title = models.CharField(max_length=150, null=False,
                             blank=False, help_text=_("Server Title"))
    url = models.URLField(blank=False, null=False,
                          help_text=_("Base Server URL"))
    content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    connection = GenericForeignKey('content_type', 'object_id')
    refresh_interval = models.DurationField(default=timezone.timedelta(days=7))
    operations = JSONField(default=dict, blank=True)

    @cached_property
    def server_handler_key(self):
        key = None
        for server in SUPPORTED_SERVERS:
            if server.value == self.server_type:
                key = server.name
        return key

    @cached_property
    def handler(self):
        handler = None
        Handler = get_handler_class_handler(
            self.server_handler_key, server=True)
        handler = Handler(self.url, self.id)
        return handler

    @property
    def is_alive(self):
        alive = False
        handler = self.handler
        if handler:
            alive = handler.is_alive
        return alive

    def __str__(self):
        return self.url


class SimpleAuthConnection(BaseConnectionModel):
    BASIC_HANDLER_KEY = "BASIC"
    DIGEST_HANDLER_KEY = "DIGEST"
    AUTH_TYPES = (
        (BASIC_HANDLER_KEY, _("Basic Authentication")),
        (DIGEST_HANDLER_KEY, _("Digest Authentication"))
    )
    username = models.CharField(
        max_length=200, null=False, blank=False, help_text=_("Server Type"))
    password = EncryptedTextField(
        null=False, blank=False, help_text=_("User Password"))
    auth_type = models.CharField(
        max_length=6, choices=AUTH_TYPES, help_text=_("Authentication Type"))
    servers = GenericRelation(Server, related_query_name='connections')

    @property
    def session(self):
        handler = get_handler_class_handler(self.auth_type)
        return handler.get_session(self)

    def __str__(self):
        return self.username

    class Meta:
        permissions = CONNECTION_PERMISSIONS


class TokenAuthConnection(BaseConnectionModel):
    TOKEN_HANDLER_KEY = "TOKEN"
    token = models.TextField(null=False, blank=False,
                             help_text=_("Access Token"))
    servers = GenericRelation(Server, related_query_name='connections')
    prefix = models.CharField(
        max_length=60, null=False, blank=True, default="Bearer",
        help_text=_("Authentication Header Value Prefix"))

    def __str__(self):
        return "<{}:{}>".format(self.prefix, self.token)

    @property
    def session(self):
        handler = get_handler_class_handler(
            TokenAuthConnection.TOKEN_HANDLER_KEY)
        return handler.get_session(self)

    class Meta:
        permissions = CONNECTION_PERMISSIONS


@receiver(post_save, sender=SimpleAuthConnection)
@receiver(post_delete, sender=SimpleAuthConnection)
def invalidate_simple_auth_cache(sender, instance, **kwargs):
    cache.delete('simple_auth')


@receiver(post_save, sender=TokenAuthConnection)
@receiver(post_delete, sender=TokenAuthConnection)
def invalidate_token_auth_cache(sender, instance, **kwargs):
    cache.delete('token_auth')


@receiver(post_save, sender=TokenAuthConnection)
@receiver(post_save, sender=SimpleAuthConnection)
def connection_post_save(sender, instance, created, **kwargs):
    if created and instance.owner and \
            instance.owner.username != settings.ANONYMOUS_USER_NAME:
        users = get_user_model().objects.filter(is_superuser=True,)
        if instance.owner:
            users = users.union(get_user_model().objects.filter(
                username=instance.owner.username))
        for user in users:
            for perm in CONNECTION_PERMISSIONS:
                assign_perm(perm[0], user, instance)
