from django.conf import settings
if settings.PRODUCTION:
    from .production import *
else:
    from .dev import *

from .. import tool
import uuid

class VMCreateOperation():
  @classmethod
  def get_operator(cls):
    if not hasattr(cls, 'operator'):
      cls.operator = VMOperator()
    return cls.operator

  def __init__(self, vm):
    self.vm = vm

  def submit(self):
    data = self.vm.get_values()
    print "passwd type ====",
    print type(data['password'])

    xml = tool.XMLGen(
      data['name'], self.get_uuid(), data['memorysize'], data['cpu'], data['os'],
      self.get_macaddr(), data['vncport'], data['password'])
    self.__class__.get_operator().create_vm(xml)
    return self

  def get_uuid(self):
    if not hasattr(self, 'uuid'):
      self.uuid = uuid.uuid4()
    return self.uuid

  def get_macaddr(self):
    if not hasattr(self, 'macaddr'):
      self.macaddr = tool.GenMac()
    return self.macaddr

class VMSearchQuery():
  @classmethod
  def get_operator(cls):
    if not hasattr(cls, 'operator'):
      cls.operator = VMOperator()
    return cls.operator

  def __init__(self, uuid):
    self.uuid = uuid

  def search(self):
    print type(self.uuid)
    attrs = self.__class__.get_operator().get_vminfo(self.uuid)
    return attrs
