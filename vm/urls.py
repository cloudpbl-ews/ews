from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.create_vm, name='new'),
    url(r'^success$', views.success, name='success'),
    url(r'^(?P<vm_id>[0-9]+)/delete$', views.delete_vm, name='delete'),
    url(r'^(?P<vm_id>[0-9]+)/edit$', views.edit, name='edit'),
    url(r'^OS-collection$', views.OScollection, name='OScollection'),
    url(r'^(?P<vm_id>[0-9]+)$', views.info, name='info'),
    url(r'^(?P<vm_id>[0-9]+)/power_on$', views.power_on_vm, name='power_on'),
    url(r'^(?P<vm_id>[0-9]+)/shutdown$', views.shutdown_vm, name='shutdown'),
]
