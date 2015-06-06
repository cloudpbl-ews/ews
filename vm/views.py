from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    name = request.user.get_username()
    return HttpResponse(name)

@login_required
def new_vm(request):
    return render(request, 'vm/new_vm.html', { 'user': request.user })

@login_required
def create(request):
    return HttpResponse('WIP')
