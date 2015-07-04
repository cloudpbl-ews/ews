from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.create_vm, name='new'),
    url(r'^success$', views.success, name='success'),
    url(r'^(?P<vm_id>[0-9]+)/delete$', views.delete_vm, name='delete'),
    url(r'^OS-collection$', views.OScollection, name='OScollection'),
    url(r'^(?P<vm_id>[0-9]+)$', views.info, name='info'),
    url(r'^(?P<vm_id>[0-9]+)/power_on$', views.power_on_vm, name='power_on'),
    url(r'^(?P<vm_id>[0-9]+)/shutdown$', views.shutdown_vm, name='shutdown'),
    url(r'^(?P<vm_id>[0-9]+)/force_shutdown$', views.force_shutdown_vm, name='force_shutdown'),
    url(r'^(?P<vm_id>[0-9]+)/hostname_edit$', views.hostname_edit, name='hostname_edit'),
    url(r'^(?P<vm_id>[0-9]+)/cpu_edit$', views.cpu_edit, name='cpu_edit'),
    url(r'^(?P<vm_id>[0-9]+)/cd_image_edit$', views.cd_image_edit, name='cd_image_edit'),
    url(r'^(?P<vm_id>[0-9]+)/bootdev_edit$', views.bootdev_edit, name='bootdev_edit'),
    url(r'^(?P<vm_id>[0-9]+)/memorysize_edit$', views.memorysize_edit, name='memorysize_edit'),
    url(r'^(?P<vm_id>[0-9]+)/attach_disk$', views.attach_disk, name='attach_disk'),
]
