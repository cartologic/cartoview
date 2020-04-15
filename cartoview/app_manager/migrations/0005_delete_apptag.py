# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0004_auto_20171002_0446'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppTag',
        ),
    ]
