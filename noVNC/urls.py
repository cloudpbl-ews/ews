from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<vm_id>[0-9]+)$', views.index, name='index'),
]
