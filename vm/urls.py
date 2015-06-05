from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new_vm, name='new'),
    url(r'^create$', views.create, name='create'),
]
