from django.conf.urls import url

from . import views

rlpatterns = [
    url(r'^$', views.index, name='index'),
]
