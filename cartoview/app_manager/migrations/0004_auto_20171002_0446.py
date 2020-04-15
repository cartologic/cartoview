# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('app_manager', '0003_auto_20171002_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='tags',
        ),
        migrations.AddField(
            model_name='app',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag',
                through='taggit.TaggedItem',
                help_text='A comma-separated list of tags.',
                verbose_name='Tags'),
        ),
    ]
