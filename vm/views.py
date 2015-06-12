from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext

from .models import CreateVM

from django.template.context_processors import csrf

from vmoperation import VMOperator

import uuid
from . import tool


@login_required
def index(request):
  template = loader.get_template('vm/index.html')
  op = VMOperator()
  vms = op.get_vm_names_state()
  print "vms"
  print vms
  vmnames = []
  for vm in vms:
    vmnames.append(vm.name())
  print vmnames
  context = Context({'vmnames': vmnames })
  return HttpResponse(template.render(context))


@login_required
def create_vm(request):
  op = VMOperator()
  if(request.method == 'POST'):
    f = CreateVM(request.POST)
    if(f.is_valid()):
      name = f.cleaned_data['name']
      memory = f.cleaned_data['memorysize']
      cpu = f.cleaned_data['cpu']
      os = f.cleaned_data['os']
      disksize  = f.cleaned_data['disksize']
      print name
      print memory
      print cpu
      print os
      print disksize
      macaddr = tool.GenMac()
      uuid_gen = uuid.uuid4()
      websocketport = "5777"
      passwd = "hoge"
      xml = tool.XMLGen(name, uuid_gen, memory, cpu, os, macaddr, websocketport, passwd)
      op.create_vm(xml)
      return HttpResponseRedirect('vm/success')
  else:
    f = CreateVM()
    return render_to_response('vm/create_vm.html', {'form': f},context_instance=RequestContext(request))

@login_required
def success(request):
    return HttpResponse('created vm successfully')
