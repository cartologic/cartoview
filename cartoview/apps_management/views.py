import pkg_resources
from StringIO import StringIO
import cartoview
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from pkg_resources import parse_version
from django.core.management import call_command
from .models import AppStore
from cartoview.apps_management.models import InstalledApps

REST_URL = AppStore.objects.all()[0].url


@csrf_exempt
def check_dep(dep_list, r):
    """this function check if dependencies compatible with current cartoview version"""
    for i, x in enumerate(dep_list):
        if i == len(dep_list):
            return
        else:
            for x in dep_list:
                q = requests.get(REST_URL + 'app/?name={}'.format(x))
                # q = requests.get('http://127.0.0.1:8000{}'.format(x))
                if pkg_resources.parse_version(
                        q.json()['objects'][0]['latest_version']["cartoview_version"]) > pkg_resources.parse_version(
                    cartoview.__version__):
                    r[
                        "message"] = "App or it's Dependencies ({}) Requires a Heigher Version Of Cartoview V{} or Later".format(
                        q.json()['objects'][0]["title"],
                        q.json()['objects'][0]['latest_version']["cartoview_version"])
                else:
                    if q.json()['objects'][0]['latest_version']["dependencies"]:
                        check_dep(q.json()["dependencies"], r)


@csrf_exempt
def check_installation(app_slug):
    """this view to check if app compatible with current cartoview version and call function to check dependencies of this app too"""
    result = {}
    r = requests.get(REST_URL + 'app/?name={}'.format(app_slug))
    if pkg_resources.parse_version(
            r.json()['objects'][0]['latest_version']['cartoview_version']) > pkg_resources.parse_version(
        cartoview.__version__):
        result["message"] = "this app requires a heigher version of cartoview v{} or later".format(
            r.json()['objects'][0]['latest_version']['cartoview_version'])
        return result
    else:
        if r.json()['objects'][0]['latest_version']["dependencies"]:
            check_dep(r.json()['objects'][0]['latest_version']["dependencies"], result)
        return result


def json_processing(apps, installed):
    """prepare Json response to view by modifying response and add app status to it i.e uptodate  outdated requires hiegher version of cartoview and installed  """
    for app in apps:
        if installed:
            for installed_app in installed:
                if app['name'] == installed_app.name:
                    app_version = parse_version(app['latest_version']['version'])
                    installed_app_version = parse_version(installed_app.version)
                    if app_version == installed_app_version:
                        app['status'] = 'Uninstall'
                        break
                    elif app_version > installed_app_version:
                        if parse_version(app['latest_version']['cartoview_version']) > parse_version(
                                cartoview.__version__):
                            app["message"] = "this app requires a heigher version of cartoview v{}".format(
                                app['latest_version']['cartoview_version'])
                        app['status'] = 'outdated'
                        break
                    else:
                        app['status'] = 'Uninstall'
                        break
                else:
                    if parse_version(app['latest_version']['cartoview_version']) > parse_version(
                            cartoview.__version__):
                        app["message"] = "this app requires a heigher version of cartoview v{}".format(
                            app['latest_version']['cartoview_version'])
                    app['status'] = 'install'
        else:
            if parse_version(app['latest_version']['cartoview_version']) > parse_version(
                    cartoview.__version__):
                app["message"] = "this app requires a heigher version of cartoview v{}".format(
                    app['latest_version']['cartoview_version'])

            app['status'] = 'install'


# Create your views here.
def home(request):
    r = requests.get(REST_URL + 'app/')
    apps = r.json()['objects']
    installed = InstalledApps.objects.all()
    json_processing(apps, installed)
    return render(request, template_name="apps_management/app_manager.html", context={'apps': apps})


@csrf_exempt
def handle_install_apps(request, name):
    """when user click install or update this view handle installation by checking app to be installed and if it satisfy reqiurements return by the proper message to user"""
    if request.is_ajax():
        result = check_installation(name)
        if result:
            result.update(status=1)
            return JsonResponse(result)
        else:
            dep = []
            r = requests.get(REST_URL + 'app/?name={}'.format(name))
            if r.json()['objects'][0]['latest_version']['dependencies']:
                for x in r.json()['objects'][0]['latest_version']['dependencies']:
                    q = requests.get(REST_URL + 'app/?name={}'.format(x))
                    dep.append(q.json()['objects'][0]['title'])
                return JsonResponse(
                    {'message': "this app requires this packages ({})".format(",".join(dep)), "status": 0})
            else:
                return JsonResponse(
                    {'message': "Are You Sure You Want to Install this App ({})".format(name), "status": 0})


@csrf_exempt
def handle_uninstall_apps(request, name):
    """this view to handle app uninstallaion"""
    r = requests.get(REST_URL + 'app/?name={}'.format(name))
    if request.is_ajax():
        out = StringIO()
        call_command('uninstall_app', name, stdout=out)
        message = out.getvalue()
        print message
        if int(message) == 0:
            return JsonResponse({'message': "{} App Successfully Uninstalled".format(r.json()['objects'][0]['title'])})
        else:
            return JsonResponse(
                {'message': "{} App not Uninstalled because an error occured".format(r.json()['objects'][0]['title'])})
    else:
        return JsonResponse({'message': "Error"})


@csrf_exempt
def confirm_app_installation(request, name):
    """if user confirm that he want to install the app"""
    dep = []
    r = requests.get(REST_URL + 'app/?name={}'.format(name))
    if r.json()['objects'][0]['latest_version']['dependencies']:
        for x in r.json()['objects'][0]['latest_version']['dependencies']:
            q = requests.get(REST_URL + 'app/?name={}'.format(x))
            dep.append(q.json()['objects'][0]['name'])
    out = StringIO()
    call_command('install_app', name, stdout=out)
    message = out.getvalue()
    if int(message.strip().split()[0]) == 1:
        if len(message.strip().split()) > 1:
            return JsonResponse(
                {'message': "{} App Successfully installed".format(r.json()['objects'][0]['title']),
                 'status': "Msuccess", 'dep': dep})
        return JsonResponse(
            {'message': "{} App Successfully installed".format(r.json()['objects'][0]['title']), 'status': "success"})
    else:
        return JsonResponse(
            {'message': "{} App not Installed".format(r.json()['objects'][0]['title']), 'status': "info"})
