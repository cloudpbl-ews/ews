from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.template.context_processors import csrf

from vmoperation import VMOperator
from .forms import CreateVM

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
  if(request.method == 'POST'):
    f = CreateVM(request.POST)
    if (f.is_valid()):
      f.create_instance(request.user).save()
      return HttpResponseRedirect('vm/success')
  else:
    f = CreateVM()
    return render_to_response('vm/create_vm.html', {'form': f}, context_instance=RequestContext(request))

@login_required
def success(request):
    return HttpResponse('created vm successfully')
