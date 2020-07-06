from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name='page'),
    path("wiki", views.found_page, name='found_page')
]
