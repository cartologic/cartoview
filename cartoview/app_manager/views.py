import os
import importlib
from urlparse import urljoin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.db.models import Max, Min, F
from django.forms.util import ErrorList
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from guardian.shortcuts import get_perms
from cartoview.app_manager.forms import AppInstanceEditForm
from geonode.base.forms import CategoryForm
from geonode.base.models import TopicCategory
from geonode.people.forms import ProfileForm
from geonode.security.views import _perms_info_json
from models import *
from django.conf import settings

import json
from geonode.utils import resolve_object, build_social_links
from django.utils.translation import ugettext as _
from django.template import RequestContext, loader
from django.core.files import File
from .installer import AppInstaller

_PERMISSION_MSG_DELETE = _("You are not permitted to delete this document")
_PERMISSION_MSG_GENERIC = _("You do not have permissions for this document.")
_PERMISSION_MSG_MODIFY = _("You are not permitted to modify this document")
_PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this document's metadata")
_PERMISSION_MSG_VIEW = _("You are not permitted to view this document")

current_folder, filename = os.path.split(os.path.abspath(__file__))
temp_dir = os.path.join(current_folder, 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def save_thumbnail(filename, image):
    thumb_folder = 'thumbs'
    upload_path = os.path.join(settings.MEDIA_ROOT, thumb_folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    with open(os.path.join(upload_path, filename), 'wb') as f:
        thumbnail = File(f)
        thumbnail.write(image)

    url_path = os.path.join(settings.MEDIA_URL, thumb_folder, filename).replace('\\', '/')
    url = urljoin(settings.SITEURL, url_path)

    return url

def get_apps_names():
    return [n for n in os.listdir(settings.APPS_DIR) if os.path.isdir(os.path.join(settings.APPS_DIR, n))]

def installed_apps():
    from .models import App
    apps = App.objects.filter()
    return apps

@staff_member_required
def manage_apps(request):
    apps = App.objects.all()
    site_apps = {}


    context = {
        'apps': apps,
        'site_apps': get_apps_names(),
    }
    print context["site_apps"]
    return render(request, 'app_manager/manage.html', context)





def index(request):
    Apps = installed_apps()
    for app in Apps:
        module = importlib.import_module(app.name)
        if hasattr(module, 'urls_dict'):
            urls_dict = getattr(module, 'urls_dict')
            if 'admin' in urls_dict.keys():
                app.admin_urls = urls_dict['admin']
            else:
                app.admin_urls = None
            if 'logged_in' in urls_dict.keys():
                app.logged_in_urls = urls_dict['logged_in']
            else:
                app.logged_in_urls = None
            if 'anonymous' in urls_dict.keys():
                app.anonymous_urls = urls_dict['anonymous']
            else:
                app.anonymous_urls = None
        else:
            app.admin_urls = app.logged_in_urls = app.anonymous_urls = None

    context = {'Apps': Apps}
    return render(request, 'app_manager/apps.html', context)


@staff_member_required
@require_POST
def install_app(request, store_id, app_name, version):
    response_data = {
        'success': False,
        'messages': []
    }
    try:
        installer = AppInstaller(app_name, store_id, version)
        installedApps = installer.install()
        response_data["success"] = True
    except Exception as ex:
        response_data["messages"].append({"type": "error", "msg": ex.message})


    return HttpResponse(json.dumps(response_data), content_type="application/json")



@staff_member_required
@require_POST
def uninstall_app(request, store_id, app_name):
    response_data = {
        "success": False,
        "errors": []
    }
    try:
        installer = AppInstaller(app_name, store_id)
        installer.uninstall()
        response_data["success"] = True
    except Exception as ex:
        response_data["errors"].append(ex.message)
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required
def move_up(request, app_id):
    app = App.objects.get(id=app_id)
    prev_app = App.objects.get(order=App.objects.filter(order__lt=app.order).aggregate(Max('order'))['order__max'])
    order = app.order
    app.order = prev_app.order
    prev_app.order = order
    app.save()
    prev_app.save()
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")


@login_required
def move_down(request, app_id):
    app = App.objects.get(id=app_id)
    next_app = App.objects.get(order=App.objects.filter(order__gt=app.order).aggregate(Min('order'))['order__min'])
    order = app.order
    app.order = next_app.order
    next_app.order = order
    app.save()
    next_app.save()
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")


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
            except:
                ajax_vars = {'success': False}
                return HttpResponse(json.dumps(ajax_vars), content_type="application/json")

    return HttpResponse(json.dumps(ajax_vars), content_type="application/json")


def _resolve_appinstance(request, appinstanceid, permission='base.change_resourcebase',
                         msg=_PERMISSION_MSG_GENERIC, **kwargs):
    """
    Resolve the document by the provided primary key and check the optional permission.
    """
    return resolve_object(request, AppInstance, {'pk': appinstanceid},
                          permission=permission, permission_msg=msg, **kwargs)


def appinstance_detail(request, appinstanceid):
    """
    The view that show details of each document
    """
    appinstance = None
    try:
        appinstance = _resolve_appinstance(
            request,
            appinstanceid,
            'base.view_resourcebase',
            _PERMISSION_MSG_VIEW)

    except Http404:
        return HttpResponse(
            loader.render_to_string(
                '404.html', RequestContext(
                    request, {
                    })), status=404)

    except PermissionDenied:
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this document.")})), status=403)

    if appinstance is None:
        return HttpResponse(
            'An unknown error has occured.',
            mimetype="text/plain",
            status=401
        )

    else:
        if request.user != appinstance.owner and not request.user.is_superuser:
            AppInstance.objects.filter(id=appinstance.id).update(popular_count=F('popular_count') + 1)
        # appinstance_links = appinstance.link_set.filter(link_type__in=['appinstance_view', 'appinstance_edit'])
        set_thumbnail_link = appinstance.link_set.filter(link_type='appinstance_thumbnail')
        context_dict = {
            'perms_list': get_perms(request.user, appinstance.get_self_resource()),
            'permissions_json': _perms_info_json(appinstance),
            'resource': appinstance,
            # 'appinstance_links': appinstance_links,
            'set_thumbnail_link': set_thumbnail_link
            # 'imgtypes': IMGTYPES,
            # 'related': related
        }

        if geonode_settings.SOCIAL_ORIGINS:
            context_dict["social_links"] = build_social_links(request, appinstance)

        if getattr(geonode_settings, 'EXIF_ENABLED', False):
            try:
                from geonode.contrib.exif.utils import exif_extract_dict
                exif = exif_extract_dict(appinstance)
                if exif:
                    context_dict['exif_data'] = exif
            except:
                print "Exif extraction failed."

        return render_to_response(
            "app_manager/appinstance_detail.html",
            RequestContext(request, context_dict))


@login_required
def appinstance_metadata(
        request,
        appinstanceid,
        template='app_manager/appinstance_metadata.html'):
    appinstance = None
    try:
        appinstance = _resolve_appinstance(
            request,
            appinstanceid,
            'base.change_resourcebase_metadata',
            _PERMISSION_MSG_METADATA)

    except Http404:
        return HttpResponse(
            loader.render_to_string(
                '404.html', RequestContext(
                    request, {
                    })), status=404)

    except PermissionDenied:
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to edit this instance.")})), status=403)

    if appinstance is None:
        return HttpResponse(
            'An unknown error has occured.',
            mimetype="text/plain",
            status=401
        )

    else:
        poc = appinstance.poc
        metadata_author = appinstance.metadata_author
        topic_category = appinstance.category

        if request.method == "POST":
            appinstance_form = AppInstanceEditForm(
                request.POST,
                instance=appinstance,
                prefix="resource")
            category_form = CategoryForm(
                request.POST,
                prefix="category_choice_field",
                initial=int(
                    request.POST["category_choice_field"]) if "category_choice_field" in request.POST else None)
        else:
            appinstance_form = AppInstanceEditForm(instance=appinstance, prefix="resource")
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
                        request.POST,
                        prefix="poc",
                        instance=poc)
                else:
                    poc_form = ProfileForm(request.POST, prefix="poc")
                if poc_form.is_valid():
                    if len(poc_form.cleaned_data['profile']) == 0:
                        # FIXME use form.add_error in django > 1.7
                        errors = poc_form._errors.setdefault('profile', ErrorList())
                        errors.append(_('You must set a point of contact for this resource'))
                        poc = None
                if poc_form.has_changed and poc_form.is_valid():
                    new_poc = poc_form.save()

            if new_author is None:
                if metadata_author is None:
                    author_form = ProfileForm(request.POST, prefix="author",
                                              instance=metadata_author)
                else:
                    author_form = ProfileForm(request.POST, prefix="author")
                if author_form.is_valid():
                    if len(author_form.cleaned_data['profile']) == 0:
                        # FIXME use form.add_error in django > 1.7
                        errors = author_form._errors.setdefault('profile', ErrorList())
                        errors.append(_('You must set an author for this resource'))
                        metadata_author = None
                if author_form.has_changed and author_form.is_valid():
                    new_author = author_form.save()

            if new_poc is not None and new_author is not None:
                the_appinstance = appinstance_form.save()
                the_appinstance.poc = new_poc
                the_appinstance.metadata_author = new_author
                the_appinstance.keywords.add(*new_keywords)
                AppInstance.objects.filter(id=the_appinstance.id).update(category=new_category)

                return HttpResponseRedirect(
                    reverse(
                        'appinstance_detail',
                        args=(
                            appinstance.id,
                        )))
            else:
                the_appinstance = appinstance_form.save()
                if new_poc is None:
                    the_appinstance.poc = appinstance.owner
                if new_author is None:
                    the_appinstance.metadata_author = appinstance.owner
                the_appinstance.keywords.add(*new_keywords)
                AppInstance.objects.filter(id=the_appinstance.id).update(category=new_category)

                return HttpResponseRedirect(
                    reverse(
                        'appinstance_detail',
                        args=(
                            appinstance.id,
                        )))

        if poc is not None:
            appinstance_form.fields['poc'].initial = poc.id
            poc_form = ProfileForm(prefix="poc")
            poc_form.hidden = True
        else:
            poc_form = ProfileForm(prefix="poc")
            poc_form.hidden = True
        if metadata_author is not None:
            appinstance_form.fields['metadata_author'].initial = metadata_author.id
            author_form = ProfileForm(prefix="author")
            author_form.hidden = True
        else:
            author_form = ProfileForm(prefix="author")
            author_form.hidden = True

        return render_to_response(template, RequestContext(request, {
            "appinstance": appinstance,
            "appinstance_form": appinstance_form,
            "poc_form": poc_form,
            "author_form": author_form,
            "category_form": category_form,
        }))


def appinstance_remove(request, appinstanceid):
    try:
        appinstance = _resolve_appinstance(
            request,
            appinstanceid,
            'base.delete_resourcebase',
            _PERMISSION_MSG_DELETE)
        appinstance.delete()
        return HttpResponseRedirect(reverse('appinstance_browse'))
    except PermissionDenied:
        return HttpResponse(
            'You are not allowed to delete this Instance',
            mimetype="text/plain",
            status=401
        )
