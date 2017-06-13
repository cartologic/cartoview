from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings


@require_http_methods(["POST", ])
def settings_api(request):
    result = {}
    data = request.POST.getlist('attributes')
    for attr in data:
        if hasattr(settings, attr):
            result[attr] = getattr(settings, attr)
        else:
            return HttpResponse("{} Not Found in settings".format(attr), status=404)
    return JsonResponse(result)
