from django.conf import settings
if settings.PRODUCTION:
    from .production import *
else:
    from .dev import *

from .. import tool
import uuid

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
          image_file = self.vm.os,
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
        # TODO: Implement update operations(disksize)
        print "hdd "+str(self.vm.disksize)

        self.__class__.get_operator().destroy(self.vm.uuid)
        self.__class__.get_operator().set_cpu(self.vm.uuid, self.vm.cpu)
        self.__class__.get_operator().set_memory(self.vm.uuid,
            self.vm.memorysize*1024*1024*1024)
        self.__class__.get_operator().start(self.vm.uuid)

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
        self.__class__.get_operator().undefine_vm(self.vm.uuid)
