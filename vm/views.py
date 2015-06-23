from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.template.context_processors import csrf

from vmoperation import VMOperator
from .forms import CreateVM, UpdateVM
from .models import VirtualMachine, VirtualMachineRecord

from django.conf import settings

import uuid
import string
import random

@login_required
def index(request):
    vm_records = request.user.virtualmachinerecord_set.all()
    vms = [VirtualMachine.from_record(vm) for vm in vm_records]
    # This `cpus` indicates which cpu data should be rendered for each vm.
    # TODO: Fetch which cpu is used by each vm.
    cpus = [1]
    return render(request, 'vm/index.html', {'vms': vms, 'cpus': cpus, 'HYPERVISOR_URL': settings.HYPERVISOR_URL})

@login_required
def create_vm(request):
    if(request.method == 'POST'):
        f = CreateVM(request.POST)
        if (f.is_valid()):
            # TODO: move these default values to models
            vncport = VirtualMachineRecord.find_vnc_port()
            passwd = random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
            f.create_instance(request.user, vncport, passwd).save()
            return HttpResponseRedirect('success')
    else:
        f = CreateVM()
        return render_to_response('vm/create_vm.html', {'form': f}, context_instance=RequestContext(request))

@login_required
def success(request):
    return render_to_response('vm/create_success.html')

@login_required
def delete_vm(request, vm_id):
    if(request.method == 'POST'):
      vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
      vm = VirtualMachine.from_record(vm_record)
      vm.delete()
      return render_to_response('vm/delete_success.html')
    else :
      return HttpResponseForbidden()

@login_required
def edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateVM(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateVM.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
