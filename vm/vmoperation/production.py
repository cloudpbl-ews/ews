#!/usr/bin/env python
# coding:utf-8
#
# vmoperation.py
#
# Author:   Hiromasa Ihara (taisyo)
# Created:  2015-06-06
#

# Notice: In this library UUID is used as vm handle.

from uuid import UUID
import os
import libvirt

class VMOperator():
  hypervisor_url = "qemu+tls://157.82.3.111/system"
  def __init__(self):
    self.con = libvirt.open(self.hypervisor_url)
    if self.con is None:
      raise

 # def __init__(self, hypervisor_uri):
 #   if hypervisor_uri is None:
 #     raise
 #   self.uri = hypervisor_uri

 #   self.con = libvirt.open(self.uri)
 #   if self.con is None:
 #     raise

  def start(self, uuid) :
    os.system("virsh -c {:s} start {:s}".format(self.hypervisor_url, str(uuid)))

  def shutdown(self, uuid) :
    os.system("virsh -c {:s} shutdown {:s}".format(self.hypervisor_url, str(uuid)))

  def reboot(self, uuid) :
    os.system("virsh -c {:s} reboot {:s}".format(self.hypervisor_url, str(uuid)))

  def show_vminfo(self, uuid) :
    vm = self.con.lookupByUUID(uuid.bytes)
    if vm is None:
      raise
    print"###############"
    print vm
    print"###############"

    infos = vm.info()
    print 'UUID = %s' % uuid
    print 'Name =  %s' % vm.name()
    print 'State = %s' % infos[0]
    print 'Max Memory = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[2]
    print ''

  def get_vminfo(self, uuid) :
    vm = self.con.lookupByUUID(uuid.bytes)
    if vm is None:
      raise

    infos = vm.info()

    return {"same":vm.name(), "state": infos[0], "memory": infos[1]}

  def get_vmlist(self) :
    vms_uuid = []
    ## Obtain running virtual machines
    running_vms = self.con.listDomainsID()
    print "runnig_vms"
    print running_vms
    for vmid in running_vms:
      uuid = UUID(bytes=self.con.lookupByID(vmid).UUID())
      vms_uuid.append(uuid)
    print "vm_uuid"
    print vms_uuid
    ## Obtain defined but not running virtual machines
    defined_vms = self.con.listDefinedDomains()
    for vmname in defined_vms:
      uuid = UUID(bytes=self.con.lookupByName(vmname).UUID())
      vms_uuid.append(uuid)
    print "vms_uuid"
    print vms_uuid
    return vms_uuid

  def get_vm_names_state(self) :
    vms = []
    ## Obtain running virtual machines
    running_vms = self.con.listDomainsID()
    for vmid in running_vms:
      uuid = UUID(bytes=self.con.lookupByID(vmid).UUID())
      vms.append(self.con.lookupByUUID(uuid.bytes))
    ## Obtain defined but not running virtual machines
    defined_vms = self.con.listDefinedDomains()
    for vmname in defined_vms:
      uuid = UUID(bytes=self.con.lookupByName(vmname).UUID())
      vms.append(self.con.lookupByUUID(uuid.bytes))
    return vms



if __name__ == '__main__':
  op = VMOperator()
  for uuid in op.get_vmlist() :
    op.show_vminfo(uuid)
    #op.start(uuid)
