# -*- coding: utf-8 -*-
# from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount, SocialToken
from cartoview.connections.models import Server, TokenAuthConnection
from cartoview.connections.tasks import harvest_task


@receiver(post_save, sender=SocialAccount)
def harvest_geonode_user_resources(sender, instance, **kwargs):
    if instance.provider == 'geonodeprovider':
        server, created = Server.objects.get_or_create(
            owner=instance.user, server_type=Server.SERVER_TYPES[4][0],
            url=settings.OAUTH_SERVER_BASEURL + '/api/layers/')
        if created:
            token = SocialToken.objects.get(account=instance)
            TokenAuthConnection.objects.create(
                server=server, owner=instance.user, token=token.token, auth_type='TOKEN')
            harvest_task.delay(server_id=server.id, user_id=instance.user.id)
