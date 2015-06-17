from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.template.context_processors import csrf

from vmoperation import VMOperator
from .forms import CreateVM
from .models import VirtualMachine, VirtualMachineRecord

import uuid
import string
import random

@login_required
def index(request):
  vm_records = request.user.virtualmachinerecord_set.all()
  vms = [VirtualMachine.from_record(vm) for vm in vm_records]
  cpus = [1]
  return render(request, 'vm/index.html', {'vms': vms, 'cpus': cpus})

@login_required
def create_vm(request):
  if(request.method == 'POST'):
    f = CreateVM(request.POST)
    if (f.is_valid()):
      vncport = VirtualMachineRecord.find_vnc_port()
      passwd = random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
      f.create_instance(request.user, vncport, passwd).save()
      return HttpResponseRedirect('vm/success')
  else:
    f = CreateVM()
    return render_to_response('vm/create_vm.html', {'form': f}, context_instance=RequestContext(request))

@login_required
def success(request):
    return render_to_response('vm/success.html')
