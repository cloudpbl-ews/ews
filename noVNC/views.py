from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader

from vm.models import VirtualMachine, VirtualMachineRecord
from django.conf import settings

@login_required
def index(request, vm_id):
    vm_record = get_object_or_404(VirtualMachineRecord, pk=vm_id)
    vm = VirtualMachine.from_record(vm_record)
    return render(request, 'noVNC/vnc_auto.html', { 'vm': vm, 'novnc_url': settings.HYPERVISOR_URL })
