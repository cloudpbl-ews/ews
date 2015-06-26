from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.create_vm, name='new'),
    url(r'^success$', views.success, name='success'),
    url(r'^(?P<vm_id>[0-9]+)/delete$', views.delete_vm, name='delete'),
    url(r'^(?P<vm_id>[0-9]+)/edit$', views.edit, name='edit'),
]
