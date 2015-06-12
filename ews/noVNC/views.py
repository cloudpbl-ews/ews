from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader

@login_required
def index(request):
  template = loader.get_template('noVNC/vnc_auto.html')
  return HttpResponse(template.render())
