# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc
import json
import os

from django.conf import settings
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.db import transaction
from django.db.models import F, Max, Min
from django.forms.utils import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from future import standard_library
from future.utils import with_metaclass
from geonode.base.forms import CategoryForm
from geonode.base.models import TopicCategory
from geonode.people.forms import ProfileForm
from geonode.security.views import _perms_info_json
from geonode.utils import build_social_links
from guardian.shortcuts import get_perms

from cartoview.app_manager.forms import AppInstanceEditForm
from cartoview.log_handler import get_logger
from .decorators import (PERMISSION_MSG_DELETE, PERMISSION_MSG_METADATA,
                         PERMISSION_MSG_VIEW, can_change_app_instance,
                         can_view_app_instance)
from .installer import AppInstaller
from .models import App, AppInstance
from .utils import AppsThumbnail, resolve_appinstance

logger = get_logger(__name__)

standard_library.install_aliases()

_PERMISSION_MSG_DELETE = _("You are not permitted to delete this document")
_PERMISSION_MSG_GENERIC = _("You do not have permissions for this document.")
_PERMISSION_MSG_MODIFY = _("You are not permitted to modify this document")
_PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this document's metadata")
_PERMISSION_MSG_VIEW = _("You are not permitted to view this document")
# TODO: remove this line after fixing apps
# NOTE: this line is here to handle if apps unsing old _resolve_appinstance
# function
_resolve_appinstance = resolve_appinstance
current_folder, filename = os.path.split(os.path.abspath(__file__))
temp_dir = os.path.join(current_folder, 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


def get_apps_names():
    apps = []
    if os.path.exists(settings.APPS_DIR):
        apps = [
            n for n in os.listdir(settings.APPS_DIR)
            if os.path.isdir(os.path.join(settings.APPS_DIR, n))
        ]
    return apps


def installed_apps():
    from .models import App
    apps = App.objects.filter().order_by('order')
    return apps


@staff_member_required
def manage_apps(request):
    from cartoview.version import get_backward_compatible, get_current_version
    from pkg_resources import parse_version
    apps = App.objects.all()
    _version = parse_version(get_current_version())._version
    release = _version.release
    version = [str(x) for x in release]
    context = {
        'apps': apps,
        'site_apps': get_apps_names(),
        'version_info': {
            'current_version': ".".join(version),
            'backward_versions': get_backward_compatible()
        }
    }
    return render(request, 'app_manager/manage.html', context)


def index(request):
    Apps = installed_apps()
    context = {'Apps': Apps}
    return render(request, 'app_manager/apps.html', context)


@staff_member_required
@require_POST
@transaction.atomic
def install_app(request, store_id, app_name, version):
    response_data = {'success': False, 'messages': []}
    # TODO: remove try
    try:
        installer = AppInstaller(app_name, store_id, version, request.user)
        installer.install()
        response_data["success"] = True
    except Exception as ex:
        logger.error(ex)
        response_data["messages"].append({"type": "error", "msg": ex})

    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


@staff_member_required
@require_POST
def uninstall_app(request, store_id, app_name):
    response_data = {"success": False, "errors": []}
    try:
        installer = AppInstaller(app_name, store_id, user=request.user)
        installer.uninstall(restart=False)
        response_data["success"] = True
    except Exception as ex:
        logger.error(ex)
        response_data["errors"].append(ex)
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


@login_required
def move_up(request, app_id):
    app = App.objects.get(id=app_id)
    prev_app = App.objects.get(
        order=App.objects.filter(
            order__lt=app.order).aggregate(Max('order'))['order__max'])
    order = app.order
    app.order = prev_app.order
    prev_app.order = order
    app.save()
    prev_app.save()
    return HttpResponse(
        json.dumps({
            "success": True
        }), content_type="application/json")


@login_required
def move_down(request, app_id):
    app = App.objects.get(id=app_id)
    next_app = App.objects.get(
        order=App.objects.filter(
            order__gt=app.order).aggregate(Min('order'))['order__min'])
    order = app.order
    app.order = next_app.order
    next_app.order = order
    app.save()
    next_app.save()
    return HttpResponse(
        json.dumps({
            "success": True
        }), content_type="application/json")


def save_app_orders(request):
    if request.method == 'POST':
        apps_list = request.POST.get('apps', None)

        if apps_list:
            try:
                apps = json.loads(apps_list)
                menu_apps = apps['menu_apps']
                non_menu_apps = apps['non_menu_apps']
                for idx, val in enumerate(menu_apps):
                    app = App.objects.get(id=int(val['id']))
                    app.order = idx
                    app.in_menu = True
                    app.save()

                for idx, val in enumerate(non_menu_apps):
                    app = App.objects.get(id=int(val['id']))
                    app.order = idx + len(menu_apps)
                    app.in_menu = False
                    app.save()
                ajax_vars = {'success': True}
            except BaseException:
                ajax_vars = {'success': False}
                return HttpResponse(
                    json.dumps(ajax_vars), content_type="application/json")

    return HttpResponse(json.dumps(ajax_vars), content_type="application/json")


def appinstance_detail(request, appinstanceid):
    """
    The view that show details of each document
    """
    appinstance = None
    try:
        appinstance = resolve_appinstance(request, appinstanceid,
                                          'base.view_resourcebase',
                                          PERMISSION_MSG_VIEW)

    except Http404:
        return render(request, '404.html', context={}, status=404)

    except PermissionDenied:
        return render(request, '401.html', context={
            'error_message':
                _("You are not allowed to view this document.")
        }, status=403)

    if appinstance is None:
        return HttpResponse(
            'An unknown error has occured.', mimetype="text/plain", status=401)

    else:
        if request.user != appinstance.owner and not request.user.is_superuser:
            AppInstance.objects.filter(id=appinstance.id).update(
                popular_count=F('popular_count') + 1)
        set_thumbnail_link = appinstance.link_set.filter(
            link_type='appinstance_thumbnail')
        context_dict = {
            'perms_list':
                get_perms(request.user, appinstance.get_self_resource()),
            'permissions_json':
                _perms_info_json(appinstance),
            'resource':
                appinstance,
            # 'appinstance_links': appinstance_links,
            'set_thumbnail_link':
                set_thumbnail_link
            # 'imgtypes': IMGTYPES,
            # 'related': related
        }

        if settings.SOCIAL_ORIGINS:
            context_dict["social_links"] = build_social_links(
                request, appinstance)

        if getattr(settings, 'EXIF_ENABLED', False):
            try:
                from geonode.contrib.exif.utils import exif_extract_dict
                exif = exif_extract_dict(appinstance)
                if exif:
                    context_dict['exif_data'] = exif
            except BaseException as e:
                logger.error(e.args[0] + "Exif extraction failed.")
        return render(request, "app_manager/appinstance_detail.html",
                      context=context_dict)


@login_required
def appinstance_metadata(request,
                         appinstanceid,
                         template='app_manager/appinstance_metadata.html'):
    appinstance = None
    try:
        appinstance = resolve_appinstance(request, appinstanceid,
                                          'base.change_resourcebase_metadata',
                                          PERMISSION_MSG_METADATA)

    except Http404:
        return render(request, '404.html', context={}, status=404)

    except PermissionDenied:
        return render(request, '401.html', context={
            'error_message': _("You are not allowed to edit this instance.")},
                      status=403)

    if appinstance is None:
        return HttpResponse(
            'An unknown error has occured.', mimetype="text/plain", status=401)

    else:
        poc = appinstance.poc
        metadata_author = appinstance.metadata_author
        topic_category = appinstance.category

        if request.method == "POST":
            appinstance_form = AppInstanceEditForm(
                request.POST, instance=appinstance, prefix="resource")
            category_form = CategoryForm(
                request.POST,
                prefix="category_choice_field",
                initial=int(request.POST["category_choice_field"])
                if "category_choice_field" in request.POST else None)
        else:
            appinstance_form = AppInstanceEditForm(
                instance=appinstance, prefix="resource")
            category_form = CategoryForm(
                prefix="category_choice_field",
                initial=topic_category.id if topic_category else None)

        if request.method == "POST" and appinstance_form.is_valid(
        ) and category_form.is_valid():
            new_poc = appinstance_form.cleaned_data['poc']
            new_author = appinstance_form.cleaned_data['metadata_author']
            new_keywords = appinstance_form.cleaned_data['keywords']
            new_category = TopicCategory.objects.get(
                id=category_form.cleaned_data['category_choice_field'])

            if new_poc is None:
                if poc is None:
                    poc_form = ProfileForm(
                        request.POST, prefix="poc", instance=poc)
                else:
                    poc_form = ProfileForm(request.POST, prefix="poc")
                if poc_form.is_valid():
                    if len(poc_form.cleaned_data['profile']) == 0:
                        # FIXME use form.add_error in django > 1.7
                        errors = poc_form._errors.setdefault(
                            'profile', ErrorList())
                        errors.append(
                            _('You must set a point of contact for this\
                             resource'))
                        poc = None
                if poc_form.has_changed and poc_form.is_valid():
                    new_poc = poc_form.save()

            if new_author is None:
                if metadata_author is None:
                    author_form = ProfileForm(
                        request.POST,
                        prefix="author",
                        instance=metadata_author)
                else:
                    author_form = ProfileForm(request.POST, prefix="author")
                if author_form.is_valid():
                    if len(author_form.cleaned_data['profile']) == 0:
                        # FIXME use form.add_error in django > 1.7
                        errors = author_form._errors.setdefault(
                            'profile', ErrorList())
                        errors.append(
                            _('You must set an author for this resource'))
                        metadata_author = None
                if author_form.has_changed and author_form.is_valid():
                    new_author = author_form.save()

            if new_poc is not None and new_author is not None:
                the_appinstance = appinstance_form.save()
                the_appinstance.poc = new_poc
                the_appinstance.metadata_author = new_author
                the_appinstance.keywords.add(*new_keywords)
                AppInstance.objects.filter(id=the_appinstance.id).update(
                    category=new_category)

                return HttpResponseRedirect(
                    reverse('appinstance_detail', args=(appinstance.id,)))
            else:
                the_appinstance = appinstance_form.save()
                if new_poc is None:
                    the_appinstance.poc = appinstance.owner
                if new_author is None:
                    the_appinstance.metadata_author = appinstance.owner
                the_appinstance.keywords.add(*new_keywords)
                AppInstance.objects.filter(id=the_appinstance.id).update(
                    category=new_category)

                return HttpResponseRedirect(
                    reverse('appinstance_detail', args=(appinstance.id,)))

        if poc is not None:
            appinstance_form.fields['poc'].initial = poc.id
            poc_form = ProfileForm(prefix="poc")
            poc_form.hidden = True
        else:
            poc_form = ProfileForm(prefix="poc")
            poc_form.hidden = True
        if metadata_author is not None:
            appinstance_form.fields[
                'metadata_author'].initial = metadata_author.id
            author_form = ProfileForm(prefix="author")
            author_form.hidden = True
        else:
            author_form = ProfileForm(prefix="author")
            author_form.hidden = True
        return render(request, template, context={
            "appinstance": appinstance,
            "appinstance_form": appinstance_form,
            "poc_form": poc_form,
            "author_form": author_form,
            "category_form": category_form,
        })


def appinstance_remove(request, appinstanceid):
    try:
        appinstance = resolve_appinstance(request, appinstanceid,
                                          'base.delete_resourcebase',
                                          PERMISSION_MSG_DELETE)
        appinstance.delete()
        return HttpResponseRedirect(reverse('appinstance_browse'))
    except PermissionDenied:
        return HttpResponse(
            'You are not allowed to delete this Instance',
            mimetype="text/plain",
            status=401)


class AppViews(with_metaclass(abc.ABCMeta, object)):
    def __init__(self, app_name):
        self.app_name = app_name
        self.new_template = "%s/new.html" % self.app_name
        self.edit_template = "%s/edit.html" % self.app_name
        self.view_template = "%s/view.html" % self.app_name

    def set_thumbnail(self, instance):
        thumbnail_obj = AppsThumbnail(instance)
        thumbnail_obj.create_thumbnail()

    def set_permissions(self, instance, access, owner):
        owner_permissions = [
            'view_resourcebase',
            'download_resourcebase',
            'change_resourcebase_metadata',
            'change_resourcebase',
            'delete_resourcebase',
            'change_resourcebase_permissions',
            'publish_resourcebase',
        ]

        if access == "private":
            permessions = {
                'users': {
                    '{}'.format(owner): owner_permissions,
                }
            }
        else:
            permessions = {
                'users': {
                    '{}'.format(owner): owner_permissions,
                    'AnonymousUser': [
                        'view_resourcebase',
                    ],
                }
            }
        # set permissions so that no one can view this appinstance other than
        #  the user
        instance.set_permissions(permessions)

    def set_keywords(self, keywords, instance):
        if hasattr(instance, 'keywords'):
            for k in keywords:
                if k not in instance.keyword_list():
                    instance.keywords.add(k)

    def save_instance(self, instance_id, owner, title, config, abstract,
                      map_id):
        if instance_id is None:
            instance_obj = AppInstance()
            instance_obj.app = App.objects.get(name=self.app_name)
            instance_obj.owner = owner
        else:
            instance_obj = AppInstance.objects.get(pk=instance_id)

        instance_obj.title = title
        instance_obj.config = config
        instance_obj.abstract = abstract
        instance_obj.map_id = map_id
        instance_obj.save()
        return instance_obj

    def save_all(self, request, instance_id=None):
        response = self.save(request, instance_id)
        id = json.loads(response.content).get('id', None)
        if id:
            instance_obj = AppInstance.objects.get(pk=id)
            thumb_obj = AppsThumbnail(instance_obj)
            thumb_obj.create_thumbnail()
        return response

    def save(self, request, instance_id=None):
        res_json = dict(success=False)
        data = json.loads(request.body)
        map_id = data.get('map', None)
        title = data.get('title', "")
        config = data.get('config', None)
        access = data.get('access', None)
        config.update(access=access)
        config = json.dumps(data.get('config', None))
        abstract = data.get('abstract', "")
        keywords = data.get('keywords', [])
        instance_obj = self.save_instance(instance_id, request.user, title,
                                          config, abstract, map_id)
        self.set_thumbnail(instance_obj)
        self.set_permissions(instance_obj, access, request.user)
        self.set_keywords(keywords, instance_obj)
        # update the instance keywords
        res_json.update(dict(success=True, id=instance_obj.id))
        return HttpResponse(
            json.dumps(res_json), content_type="application/json")

    @abc.abstractmethod
    def new(self, request, template=None, context={}, *args, **kwargs):
        """Implement New app instance View"""
        pass

    @abc.abstractmethod
    def edit(self,
             request,
             instance_id,
             template=None,
             context={},
             *args,
             **kwargs):
        """Implement Edit app instance View"""
        pass

    @abc.abstractmethod
    def view_app(self,
                 request,
                 instance_id,
                 template=None,
                 context={},
                 *args,
                 **kwargs):
        """Implement View app instance View"""
        pass

    @abc.abstractmethod
    def get_url_patterns(self):
        """implement this fuction to return you app url patterns"""
        pass


class StandardAppViews(AppViews):
    '''
    this class contains basic views for cartoview apps to use this class
    create instance ==> instance=StandardAppViews(app_name)
    then you can use class methods ==> instance.new
    '''

    def __init__(self, app_name):
        super(StandardAppViews, self).__init__(app_name)

    @method_decorator(login_required)
    def new(self, request, template=None, context={}, *args, **kwargs):
        if template is None:
            template = self.new_template
        if request.method == 'POST':
            return self.save_all(request)
        context.update(app_name=self.app_name)
        return render(request, template, context)

    @method_decorator(login_required)
    @method_decorator(can_change_app_instance)
    def edit(self,
             request,
             instance_id,
             template=None,
             context={},
             *args,
             **kwargs):
        if template is None:
            template = self.edit_template
        if request.method == 'POST':
            return self.save_all(request, instance_id)

        instance = get_object_or_404(AppInstance, pk=instance_id)
        context.update(instance=instance, app_name=self.app_name)
        return render(request, template, context)

    @method_decorator(can_view_app_instance)
    def view_app(self, request, instance_id, template=None, context={}):
        if template is None:
            template = self.view_template
        instance = get_object_or_404(AppInstance, pk=instance_id)
        context.update({"instance": instance, "app_name": self.app_name})
        return render(request, template, context)

    def get_url_patterns(self):
        return [
            url(r'^new/$', self.new, name='%s.new' % self.app_name),
            url(r'^(?P<instance_id>\d+)/edit/$',
                self.edit,
                name='%s.edit' % self.app_name),
            url(r'^(?P<instance_id>\d+)/view/$',
                self.view_app,
                name='%s.view' % self.app_name)
        ]
