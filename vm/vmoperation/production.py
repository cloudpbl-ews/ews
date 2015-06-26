#!/usr/bin/env python
# coding:utf-8
#
# vmoperation.py
#
# Author:   Hiromasa Ihara (taisyo)
# Created:  2015-06-06
#

# Notice: In this library UUID is used as vm handle.

import os
import libvirt
from uuid import UUID
from django.conf import settings
from xml.etree import ElementTree as ET

class VMOperator():
    hypervisor_url = "qemu+tls://" + settings.HYPERVISOR_URL + "/system"
    def __init__(self):
        self.con = libvirt.open(self.hypervisor_url)
        if self.con is None:
            raise

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


    def create_storage(self, xml) :
        self.con.storagePoolLookupByName("default").createXML(xml)

    def define_vm(self, xml) :
        self.con.defineXML(xml)

    def start_by_hostname(self, hostname) :
        self.con.lookupByName(hostname).create()

    def destroy(self, uuid) :
        os.system("virsh -c {:s} destroy {:s}".format(self.hypervisor_url, str(uuid)))

    def get_vminfo(self, uuid) :
        print "uuid", uuid
        vm = self.con.lookupByUUID(uuid.bytes)
        if vm is None:
            raise

        infos = vm.info()

        # TODO: Returns disksize also.
        return {"name":vm.name(), "state": infos[0], "memorysize": infos[1], 'cpu': infos[3]}

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

    def set_cpu(self, uuid, cpu_num) :
        vm = self.con.lookupByUUID(uuid.bytes)
        xml = ET.fromstring(vm.XMLDesc(0))
        vcpu_element = xml.find('./vcpu')
        vcpu_element.text = str(cpu_num)
        self.con.defineXML(ET.tostring(xml))

    def set_memory(self, uuid, memory_size) :
        vm = self.con.lookupByUUID(uuid.bytes)
        xml = ET.fromstring(vm.XMLDesc(0))
        memory_element = xml.find('./memory')
        memory_element.attrib['unit']= 'Kib'
        memory_element.text = str(memory_size/1024)
        currentmemory_element = xml.find('./currentMemory')
        currentmemory_element.attrib['unit']= 'Kib'
        currentmemory_element.text = str(memory_size/1024)
        self.con.defineXML(ET.tostring(xml))

    def get_cpu(self, uuid) :
        vm = self.con.lookupByUUID(uuid.bytes)
        xml = ET.fromstring(vm.XMLDesc(0))
        graphic_element = xml.find('./vcpu')
        return int(graphic_element.text)

    def get_memory(self, uuid) :
        vm = self.con.lookupByUUID(uuid.bytes)
        xml = ET.fromstring(vm.XMLDesc(0))
        graphic_element = xml.find('./memory')
        if graphic_element.attrib['unit'] == "KiB" :
            return int(graphic_element.text)*1024
        elif graphic_element.attrib['unit'] == "MiB" :
            return int(graphic_element.text)*1024*1024
        elif graphic_element.attrib['unit'] == "GiB" :
            return int(graphic_element.text)*1024*1024*1024

    def set_vnc_port(self, uuid, port) :
        vm = self.con.lookupByUUID(uuid.bytes)
        xml = ET.fromstring(vm.XMLDesc(0))
        graphic_element = xml.find('.//graphics')
        graphic_element.attrib['websocket'] = str(port)
        dom.updateDeviceFlags(ET.tostring(graphic_element), 0)
        self.con.defineXML(ET.tostring(xml))

if __name__ == '__main__':
    op = VMOperator()
    for uuid in op.get_vmlist() :
        op.show_vminfo(uuid)
        #op.start(uuid)
