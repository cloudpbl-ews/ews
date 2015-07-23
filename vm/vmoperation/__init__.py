from django.conf import settings
if settings.PRODUCTION:
    from .production import *
else:
    from .dev import *

from .. import tool
import uuid
import os.path

class VMOperationBase():
    @classmethod
    def get_operator(cls):
        if not hasattr(cls, 'operator'):
            cls.operator = VMOperator()
        return cls.operator

class VMCreateOperation(VMOperationBase):
    def __init__(self, vm):
        self.vm = vm

    def submit(self):
        self._define_storage()
        self._define_vm()
        self._start()
        return self

    # TODO: move this method to models
    def get_uuid(self):
        if not hasattr(self, 'uuid'):
            self.uuid = uuid.uuid4()
        return self.uuid

    # TODO: move this method to models
    def get_macaddr(self):
        if not hasattr(self, 'macaddr'):
            self.macaddr = tool.GenMac()
        return self.macaddr

    def _define_storage(self):
        storagexml = tool.StorageXMLGen(self.vm.name, self.vm.get_disksize_byte())
        print storagexml
        self.__class__.get_operator().create_storage(storagexml)

    def _define_vm(self):
        vmxml = tool.VMXMLGen(
          hostname = self.vm.name,
          uuid = self.get_uuid(),
          memorysize = self.vm.get_memorysize_kilobyte(),
          cpu = self.vm.cpu,
          image_file = self.vm.cdrom,
          macaddr = self.get_macaddr(),
          websocketport = self.vm.vncport,
          passwd = self.vm.password)
        print vmxml
        self.__class__.get_operator().define_vm(vmxml)

    def _start(self):
        self.__class__.get_operator().start_by_hostname(self.vm.name)

class VMUpdateOperation(VMOperationBase):
    def __init__(self, vm):
        self.vm = vm

    def submit(self):
        self.__class__.get_operator().force_shutdown(self.vm.uuid)
        self.__class__.get_operator().set_cpu(self.vm.uuid, self.vm.cpu)
        self.__class__.get_operator().set_memory(self.vm.uuid,
            self.vm.memorysize*1024*1024*1024)
        self.__class__.get_operator().set_bootdev(self.vm.uuid,
            self.vm.bootdev)
        self.__class__.get_operator().set_cdrom(self.vm.uuid,
            self.vm.cdrom)
        self.__class__.get_operator().start(self.vm.uuid)

class VMFetchOperation(VMOperationBase):
    def __init__(self, vm):
        self.vm = vm

    def submit(self):
        self.vm.cpu = self.__class__.get_operator().get_cpu(self.vm.uuid)
        self.vm.memorysize = self.__class__.get_operator().get_memory(self.vm.uuid)/(1024*1024*1024)
        self.vm.bootdev = self.__class__.get_operator().get_bootdev(self.vm.uuid)
        self.vm.cdrom = self.__class__.get_operator().get_cdrom(self.vm.uuid)
        self.vm.os = os.path.basename(self.vm.cdrom)
        self.vm.interfaces = self.__class__.get_operator().get_interfaces(self.vm.uuid)

class VMSearchQuery(VMOperationBase):
    def __init__(self, uuid):
        self.uuid = uuid

    def search(self):
        print type(self.uuid)
        attrs = self.__class__.get_operator().get_vminfo(self.uuid)
        return attrs

class VMDeleteOperation(VMOperationBase):
    def __init__(self, vm):
        self.vm = vm

    def submit(self):
        self.__class__.get_operator().force_shutdown(self.vm.uuid)
        storages = self.__class__.get_operator().get_storages_info_by_vm(self.vm.uuid)
        for storage in storages :
            self.__class__.get_operator().delete_storage(storage['path'])
        self.__class__.get_operator().undefine_vm(self.vm.uuid)

class VMPowerControl(VMOperationBase):
    def __init__(self, vm):
        self.vm = vm

    def power_on(self):
        self.__class__.get_operator().start(self.vm.uuid)

    def shutdown(self):
        self.__class__.get_operator().shutdown(self.vm.uuid)

class VMStorageSearchQuery(VMOperationBase):
    @classmethod
    def by_vm(cls, vm):
        return cls(vm.uuid)

    def __init__(self, vm_uuid):
        self.vm_uuid = vm_uuid

    def search(self):
        return self.__class__.get_operator().get_storages_info_by_vm(self.vm_uuid)
