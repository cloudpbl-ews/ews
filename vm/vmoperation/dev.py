
class VMOperator():
  def create_vm(self, xml):
    print 'vm_created: '
    print xml

  def get_vminfo(self, uuid) :
    return {"name": uuid, "state": 'Stop', "memorysize": '4000'}
