import sys
import os
import re
import random

from xml.etree import ElementTree as ET

### CONSTANTS ###
NETWORK_PRIVATE = 0
NETWORK_BRIDGE = 1


def GenMac():
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def StorageXMLGen(hostname, disksize):
    xml_str = """
<volume type='file'>
  <name>{hostname:s}.img</name>
  <key>_</key>
  <source>
  </source>
  <capacity unit='bytes'>_</capacity>
  <allocation unit='bytes'>_</allocation>
  <target>
    <path>_</path>
    <format type='raw'/>
    <permissions>
      <mode>0600</mode>
      <owner>107</owner>
      <group>112</group>
    </permissions>
  </target>
</volume>"""

    xml = ET.fromstring(xml_str)
    #name
    name_element = xml.find('./name')
    name_element.text = '{:s}.img'.format(hostname)
    #disksize
    capacity_element = xml.find('./capacity')
    capacity_element.text = '{:d}'.format(disksize)
    allocation_element = xml.find('./allocation')
    allocation_element.text = '{:d}'.format(disksize)
    #path
    path_element = xml.find('.//path')
    path_element.text = '/var/lib/libvirt/images/{:s}.img'.format(hostname)

    return ET.tostring(xml)

def VMXMLGen(hostname, uuid, memorysize, cpu, image_file, macaddr, websocketport, passwd):
      #<source file='/root/vmimage/{hostname:s}.img'/>
    xml_str = """
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
  <name>_</name>
  <uuid>_</uuid>
  <memory unit='KiB'>_</memory>
  <currentMemory unit='KiB'>_</currentMemory>
  <vcpu placement='static'>_</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-1.7'>hvm</type>
    <boot dev='hd'/>
    <boot dev='cdrom'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
  <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='_'/>
      <target dev='hda' bus='ide'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu'/>
      <source file='_' />
      <target dev='hdc' bus='ide'/>
      <readonly/>
    </disk>
    <controller type='usb' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>
    </controller>
    <controller type='pci' index='0' model='pci-root'/>
    <controller type='ide' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
    </controller>
    <interface type='bridge'>
      <mac address='_'/>
      <source bridge='br0'/>
      <model type='e1000'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type="vnc"  websocket="_" passwd="_" listen="0.0.0.0"/>
    <sound model='ich6'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </sound>
    <video>
      <model type='cirrus' vram='9216' heads='1'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </memballoon>
  </devices>
</domain>"""

    xml = ET.fromstring(xml_str)
    #name
    name_element = xml.find('./name')
    name_element.text = '{:s}'.format(hostname)
    #uuid
    uuid_element = xml.find('./uuid')
    uuid_element.text = '{:s}'.format(uuid)
    #memory
    memory_element = xml.find('./memory')
    memory_element.text = '{:d}'.format(memorysize)
    currentMemory_element = xml.find('./currentMemory')
    currentMemory_element.text = '{:d}'.format(memorysize)
    #cpu
    vcpu_element = xml.find('./vcpu')
    vcpu_element.text = '{:d}'.format(cpu)
    #hd
    for disk_element in xml.findall('.//disk') :
        if disk_element.attrib['device'] == 'disk' :
            source_element = disk_element.find('./source')
            source_element.attrib['file'] = '/var/lib/libvirt/images/{:s}.img'.format(hostname)
        #cdrom
        if disk_element.attrib['device'] == 'cdrom' :
            source_element = disk_element.find('./source')
            source_element.attrib['file'] = '{:s}'.format(image_file)
    #if
    interface_element = xml.find('.//interface')
    mac_element = interface_element.find('./mac')
    mac_element.attrib['address']= '{:s}'.format(macaddr)
    #vnc
    graphics_element = xml.find('.//graphics')
    graphics_element.attrib['websocket']= '{:d}'.format(websocketport)
    graphics_element.attrib['passwd']= '{:s}'.format(passwd)

    return ET.tostring(xml)

# Generate xml of network interface card for virtual machine
# type: contant, source: the name of bridge or network, model: 'virtio' or 'e1000'
def gen_nic_xml(type, source, model):
    network_xml = ET.Element('interface')
    source_xml = ET.SubElement(network_xml, 'source')
    model_xml = ET.SubElement(network_xml, 'model')
    if type == NETWORK_BRIDGE:
        iface_type = 'bridge'
        source_xml.set('bridge', source)
    elif type == NETWORK_PRIVATE:
        iface_type = 'network'
        source_xml.set('network', source)
    else:
        raise Exception("Invalid Network Type!")
    network_xml.set('type',iface_type)
    model_xml.set('type', model)
    ET.dump(network_xml)

if __name__ == '__main__':
    print gen_nic_xml(NETWORK_BRIDGE, 'br0', 'virtio')
