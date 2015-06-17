
class VMOperator():
  def create_vm(self, xml):
    print 'vm_created: '
    print xml

  def get_vminfo(self, uuid) :
    return {"name": uuid, "state": 'Stop', "memorysize": '4000'}

  def create_storage(self, xml):
    print 'storage_created: '
    print xml

  def define_vm(self, xml):
    print 'define_vm: '
    print xml

  def start_by_hostname(self, hostname):
    print 'vm_: '
    print hostname
