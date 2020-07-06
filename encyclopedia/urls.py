from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name='page'),
    path("wiki", views.found_page, name='found_page'),
    path("create_page", views.create_page, name='create_page'),
    path("save_page", views.save_page, name='save_page')
]
