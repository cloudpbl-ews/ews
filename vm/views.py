from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.template.context_processors import csrf
from django.contrib import messages

from vmoperation import VMOperator
from .forms import CreateVM, UpdateHostname, UpdateCPU, UpdateCDImage, UpdateBootdev, UpdateMemorysize, AttachDisk
from .models import VirtualMachine, VirtualMachineRecord

from django.conf import settings

import uuid
import string
import random

@login_required
def index(request):
    vm_records = request.user.virtualmachinerecord_set.all()
    vms = [VirtualMachine.from_record(vm) for vm in vm_records]
    vms_for_index = []
    for vm in vms:
        cpulist = []
        for i in range(1, vm.cpu+1):
            cpulist.append(i)
        vms_for_index.append({"vm":vm, "cpulist":cpulist})
    return render(request, 'vm/index.html', {'vms_for_index': vms_for_index, 'HYPERVISOR_URL': settings.HYPERVISOR_URL})

@login_required
def create_vm(request):
    if(request.method == 'POST'):
        f = CreateVM(request.POST)
        if (f.is_valid()):
            # TODO: move these default values to models
            vncport = VirtualMachineRecord.find_vnc_port()
            passwd = random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
            f.create_instance(request.user, vncport, passwd).save()
            messages.success(request, 'Created VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        messages.error(request, 'Failed to create VM.')
        return render(request, 'vm/new.html', {'form': f})
    else:
        f = CreateVM()
        return render(request, 'vm/new.html', {'form': f})

@login_required
def success(request):
    return render_to_response('vm/create_success.html')

@login_required
def delete_vm(request, vm_id):
    if(request.method == 'POST'):
        vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
        vm = VirtualMachine.from_record(vm_record)
        vm.delete()
        messages.success(request, 'Deleted VM successfully.')
        return HttpResponseRedirect(reverse('vm:index'))
    else :
        return HttpResponseForbidden()

OSlist = ["CentOS", "debian", "FreeBSD", "ubuntu", "arch", "Gentoo", "rasbian", "archbsd", "openbsd", "netbsd", "android"]
def isCollect(osname, vms):
    for vm in vms:
        if osname in vm.cdrom :
            return True
    return False

@login_required
def OScollection(request):
    vm_records = request.user.virtualmachinerecord_set.all()
    vms = [VirtualMachine.from_record(vm) for vm in vm_records]
    collectlist = []
    for OS in OSlist:
        collectlist.append({"name":OS, "have":isCollect(OS, vms)})
    return render(request, 'vm/OScollection.html', {"oslist": collectlist})

@login_required
def power_on_vm(request, vm_id):
    if(request.method == 'POST'):
        vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
        vm = VirtualMachine.from_record(vm_record)
        vm.power_on()
        messages.success(request, 'Started VM successfully.')
        return HttpResponseRedirect(reverse('vm:index'))
    else :
        return HttpResponseForbidden()

@login_required
def shutdown_vm(request, vm_id):
    if(request.method == 'POST'):
        vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
        vm = VirtualMachine.from_record(vm_record)
        vm.shutdown()
        messages.success(request, 'Shutdowned VM successfully.')
        return HttpResponseRedirect(reverse('vm:index'))
    else :
        return HttpResponseForbidden()

@login_required
def info(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    forms = {
        'hostname': UpdateHostname.from_model(vm),
        'cpu': UpdateCPU.from_model(vm),
        'cd_image': UpdateCDImage.from_model(vm),
        'bootdev': UpdateBootdev.from_model(vm),
        'memorysize': UpdateMemorysize.from_model(vm),
    }
    return render(request, 'vm/info.html', {'vm': vm, 'forms': forms })

@login_required
def hostname_edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateHostname(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateHostname.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})


@login_required
def cpu_edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateCPU(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateCPU.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})

@login_required
def cd_image_edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateCDImage(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateCDImage.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})

@login_required
def bootdev_edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateBootdev(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateBootdev.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})

@login_required
def memorysize_edit(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = UpdateMemorysize(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = UpdateMemorysize.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})

@login_required
def attach_disk(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    if(request.method == 'POST'):
        f = AttachDisk(request.POST)
        if f.is_valid():
            f.apply_update(vm)
            vm.save()
            messages.success(request, 'Updated VM successfully.')
            return HttpResponseRedirect(reverse('vm:index'))
        else:
            messages.error(request, 'Failed to update VM.')
            return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
    else:
        f = AttachDisk.from_model(vm)
        return render(request, 'vm/edit.html', {'form': f, 'vm': vm})
