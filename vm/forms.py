from django import forms
from .models import VirtualMachine

class CreateVM(forms.Form):
  name = forms.CharField()
  memorysize = forms.ChoiceField(initial="1", choices = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)])
  cpu = forms.ChoiceField(initial="1", choices = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)])
  os = forms.ChoiceField(choices = [("FreeBSD10.1", "FreeBSD10.1"), ("Ubuntu14.04", "Ubuntu14.04"), ("Ubuntu12.04", "Ubuntu12.04"), ("Arch", "Arch"), ("debian8.0", "debian8.0")])
  disksize = forms.IntegerField(initial="1024")
  password = forms.CharField(initial="hoge")
  vncport = forms.CharField(initial="5777")

  def create_instance(self, user):
    attributes = self.cleaned_data
    attributes['user'] = user
    return VirtualMachine(attributes=attributes)
