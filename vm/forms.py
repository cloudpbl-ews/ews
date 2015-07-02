from django import forms
from .models import VirtualMachine

name_field = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

memorychoice = [(1,"1G"),(2,"2G"),(3,"3G"),(4,"4G"),(5,"5G"),(6,"6G"),(7,"7G"),(8,"8G")]
memory_field = forms.ChoiceField(
                   initial="1",
                   choices = memorychoice,
                   widget=forms.Select(attrs={'class': 'selectpicker'}))

cpu_field = forms.ChoiceField(
                initial="1",
                choices = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)],
                widget=forms.Select(attrs={'class': 'selectpicker'}))

oschoice = [
    ('CentOS',(
        ("CentOS-6.3-x86_64-minimal.iso", "CentOS-6.3-x86_64"),
        ("CentOS-6.6-x86_64-minimal.iso", "CentOS-6.6-x86_64"),
        )
    ),
    ('debian',(
        ("debian-6.0.5-amd64-i386-netinst.iso", "debian-6.0.5-amd64"),
        ("debian-8.0.0-amd64-netinst.iso", "debian-8.0.0-amd64"),
        )
    ),
    ('FreeBSD', (
        ("FreeBSD-8.2-RELEASE-amd64-bootonly.iso", "FreeBSD-8.2-RELEASE"),
        ("FreeBSD-8.3-RELEASE-amd64-bootonly.iso", "FreeBSD-8.3-RELEASE"),
        ("FreeBSD-9.3-RELEASE-amd64-disc1.iso", "FreeBSD-9.3-RELEASE"),
        ("FreeBSD-10.1-RELEASE-amd64-bootonly.iso", "FreeBSD-10.1-RELEASE"),
        )
    ),
    ('ubuntu', (
        ("ubuntu-12.04-server-amd64.iso", "ubuntu-12.04-amd64"),
        ("ubuntu-14.04.2-server-amd64.iso", "ubuntu-14.04.2-amd64"),
        )
    ),
    ('other',(
        ("archlinux-2015.06.01-dual.iso", "archlinux-2015.06.01"),
        ("Gentoo-install-amd64-minimal-20120223.iso", "Gentoo-install-amd64-minimal-20120223"),
        )
    )
]
os_field = forms.ChoiceField(
               choices = oschoice,
               widget= forms.Select(attrs={'class': 'selectpicker', 'data-width':'auto'}))

disksize_field = forms.IntegerField(
                     initial="50",
                     widget=forms.NumberInput(
                                attrs={'class' : 'form-control', 'data-width':'auto'}))

bootdev_field = forms.ChoiceField(
                    initial= "cdrom",
                    choices = [("cdrom","CD-ROM"),("hd","HDD")],
                    widget= forms.Select(attrs={'class': 'selectpicker', 'data-width':'auto'}))


class CreateVM(forms.Form):
    name = name_field
    memorysize = memory_field
    cpu = cpu_field
    os = os_field
    disksize = disksize_field

    def create_instance(self, user, vncport, passwd):
        attributes = self.cleaned_data
        attributes['user'] = user
        attributes['vncport'] = vncport
        attributes['password'] = passwd
        return VirtualMachine(attributes=attributes)


class UpdateHostname(forms.Form):
    name = name_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'name': vm.name,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


class UpdateCPU(forms.Form):
    cpu = cpu_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'cpu': vm.cpu,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


class UpdateCDImage(forms.Form):
    os = os_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'os': vm.os,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


class UpdateBootdev(forms.Form):
    bootdev = bootdev_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'bootdev': vm.bootdev,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


class UpdateMemorysize(forms.Form):
    memorysize = memory_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'memorysize': vm.memorysize,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


class AttachDisk(forms.Form):
    disksize = disksize_field

    @classmethod
    def from_model(cls, vm):
        return cls(initial={
          'disksize': 10,
          })

    def apply_update(self, vm):
        return vm.update(self.cleaned_data)


