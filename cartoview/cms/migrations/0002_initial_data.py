# -*- coding: utf-8 -*-
from django.db import migrations
from wagtail.core.models import Page, Site


def initial_data(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    HomePage = apps.get_model('cms.HomePage')

    try:
        default_home = Page.objects.filter(title="Welcome to your new Wagtail site!")[0]
        default_home.delete()
    except:
        pass

    # Create page content type
    page_content_type, created = ContentType.objects.get_or_create(
        model='homepage',
        app_label='cms'
    )

    try:
        homepage = Page.objects.filter(title="Welcome to Cartoview!")[0]
    except:
        # Create homepage
        homepage = HomePage.objects.create(
            title="Welcome to Cartoview!",
            slug='home',
            content_type=page_content_type,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )

    # Modify default site
    try:
        Site.objects.get(id=1)
    except:
        Site.objects.create(
            id=1,
            hostname='localhost',
            port=80,
            site_name='localhost',
            root_page_id=homepage.id,
            is_default_site=True
        )
    site = Site.objects.get(id=1)
    site.root_page_id = homepage.id
    site.save()


def remove_initial_data(apps, schema_editor):
    try:
        site = Site.objects.get(id=1)
        site.delete()
    except:
        pass

    try:
        homepage = Page.objects.filter(title="Welcome to Cartoview!")[0]
        homepage.delete()
    except:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_data, remove_initial_data),
    ]
