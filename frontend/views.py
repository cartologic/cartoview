from django.shortcuts import render
from cartoview.version import json_version_info, get_current_version
# Create your views here.
from django.http import JsonResponse


def index(request):
    return render(request, 'frontend/index.html')


# endpoint to get the current cartoview version and access it from frontend
# access : public
# url: /get_version
# method : GET
def get_cartoview_version(request):
    version = get_current_version()
    # version = "1.32.dev20210518144544"
    # split version
    version = version.split('.dev')[0]
    version += '.0' if(len(version) == 4) else ''
    data = {
        'version': version
    }
    return JsonResponse(data)
