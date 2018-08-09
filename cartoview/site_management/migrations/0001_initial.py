# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cartoview.site_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteLogo',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
                ('logo',
                 models.ImageField(
                     upload_to=cartoview.site_management.
                     models.get_site_logo_path)),
                ('site',
                 models.OneToOneField(
                     to='sites.Site')),
            ],
        ),
    ]
