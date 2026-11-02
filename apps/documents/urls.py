from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_document),
    path("<int:doc_id>/extract/", views.extract),
    path("batch_extract/", views.batch_extract),
]
