"""ews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import TemplateView
from . import signals

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),
    url(r'^vm/', include('vm.urls', namespace="vm")),
    url(r'^noVNC/', include('noVNC.urls', namespace="noVNC")),
    url(r'^OScollection/', include('vm.urls', namespace="OScollection")),
]
