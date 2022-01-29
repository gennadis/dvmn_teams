from django.http import HttpResponse


def index(request):
    html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/532j-186xEQ?start=30" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    return HttpResponse(html)
