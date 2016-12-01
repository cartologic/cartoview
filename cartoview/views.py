from django.shortcuts import render, render_to_response


def index(request):
    context = {}
    return render(request, 'site_index.html', context)

