
class VMOperator():
    def destroy(self, uuid):
        print 'destroy: '
        print uuid

    def start(self, uuid):
        print 'poweron: '
        print uuid

    def shutdown(self, uuid):
        print 'shutdown: '
        print uuid

    def create_vm(self, xml):
        print 'vm_created: '
        print xml

    def get_vminfo(self, uuid) :
        return {"state": 1, 'cpu': 1, "memorysize": 4000, 'disksize': 50}

    def create_storage(self, xml):
        print 'storage_created: '
        print xml

    def define_vm(self, xml):
        print 'define_vm: '
        print xml

    def undefine_vm(self, uuid) :
        print 'undefine_vm: '
        print uuid

    def start_by_hostname(self, hostname):
        print 'vm_: '
        print hostname

    def set_cpu(self, uuid, cpu_num) :
        print 'set_cpu: '
        print uuid
        print cpu_num

    def set_memory(self, uuid, memory_size_mb) :
        print 'set_memory: '
        print uuid
        print memory_size_mb

    def set_bootdev(self, uuid, bootdev) :
        print 'set_bootdev: '
        print uuid
        print bootdev

    def get_cpu(self, uuid) :
        print 'get_cpu: '
        print uuid
        return 1

    def get_memory(self, uuid) :
        print 'get_memory: '
        print uuid
        return 2000

    def get_bootdev(self, uuid) :
        print 'get_bootdev: '
        print uuid
        return 'hd'

    def get_cdrom(self, uuid) :
        print 'get_cdrom: '
        print uuid
        return 'path/to/isofile'

    def set_cdrom(self, uuid, cdrom) :
        print 'set_cdrom: '
        print uuid
        print cdrom
