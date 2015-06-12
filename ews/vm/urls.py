from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'create_vm$', views.create_vm, name='new'),
    url(r'success$', views.success, name='success'),
]
