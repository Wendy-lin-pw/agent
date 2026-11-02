from django.contrib.staticfiles.views import serve as serve_static
from django.http import JsonResponse
from django.urls import include, path


def index(request):
    return JsonResponse({"app": "cs-teaching-agent", "docs": "/api/"})


urlpatterns = [
    path("", index),
    path("api/documents/", include("apps.documents.urls")),
    path("api/", include("apps.knowledge.urls")),
]
