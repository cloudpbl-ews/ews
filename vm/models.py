from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .vmoperation import VMCreateOperation, VMSearchQuery

class VirtualMachine():
  """
  Having full information about a virtual machine
  from the database and the hypervisor.
  """
  @classmethod
  def from_record(cls, record):
    res = VMSearchQuery(record.uuid).search()
    return cls(instance=record, attributes=res)

  def __init__(self, instance=None, attributes={}):
    self.instance = instance
    if not instance is None:
      attrs = {}
      attrs.update(model_to_dict(instance))
      attrs.update(attributes)
      attributes = attrs
    self.attributes = attributes
    self._set_attrs()

  def _set_attrs(self):
    keys = ['name', 'uuid', 'vncport', 'password', 'state', 'memorysize', 'os', 'password', 'vncport']
    for key in keys:
      if self.attributes.has_key(key):
        self.__dict__[key] = self.attributes[key]

  def to_record(self):
    if self.instance is None:
      self.instance = VirtualMachineRecord.from_virtual_machine(self)
    return self.instance

  def save(self):
    if self.is_new():
      self.attributes['uuid'] = VMCreateOperation(self).submit().get_uuid()
    else:
      # TODO: Update attributes
      pass
    self.to_record().save()
    return self

  def is_new(self):
    return not self.attributes.has_key('uuid')

  def get_uuid(self):
    return self.attributes.get('uuid')

  def get_user(self):
    return self.attributes.get('user')

  def get_values(self, keys=None):
    if keys is None:
      keys = self.attributes.keys()
    values = {}
    for key in keys:
      values[key] = self.attributes[key]
    return values

class VirtualMachineRecord(models.Model):
  """ A record class whose instance is saved in the database. """
  user = models.ForeignKey(User)
  name = models.CharField(max_length=100, default='your virtual machine')
  uuid = models.CharField(max_length=100)
  vncport = models.CharField(max_length=100)
  password = models.CharField(max_length=100)

  @classmethod
  def from_virtual_machine(cls, vm):
    user = vm.get_user()
    attrs = vm.get_values(['name', 'uuid', 'vncport', 'password'])
    return cls.objects.create(user=user, **attrs)

  def __unicode__(self):
    return self.name
