# Generated by Django 2.1.3 on 2019-02-18 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='app',
            options={'ordering': ['order'], 'permissions': (('install_app', 'Install App'), ('uninstall_app', 'Uninstall App'), ('change_state', 'Change App State (active, suspend)'))},
        ),
    ]
