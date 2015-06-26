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
    return """
<volume type='file'>
  <name>{hostname:s}.img</name>
  <key> /var/lib/libvirt/images/{hostname:s}.img</key>
  <source>
  </source>
  <capacity unit='bytes'>{disksize:d}</capacity>
  <allocation unit='bytes'>{disksize:d}</allocation>
  <target>
    <path>/var/lib/libvirt/images/{hostname:s}.img</path>
    <format type='raw'/>
    <permissions>
      <mode>0600</mode>
      <owner>107</owner>
      <group>112</group>
    </permissions>
  </target>
</volume>""".format(hostname=hostname,
        disksize=disksize)


def VMXMLGen(hostname, uuid, memorysize, cpu, image_file, macaddr, websocketport, passwd):
      #<source file='/root/vmimage/{hostname:s}.img'/>
    return """
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
  <name>{hostname:s}</name>
  <uuid>{uuid:s}</uuid>
  <memory unit='KiB'>{memorysize:d}</memory>
  <currentMemory unit='KiB'>{memorysize:d}</currentMemory>
  <vcpu placement='static'>{cpu:s}</vcpu>
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
      <source file='/var/lib/libvirt/images/{hostname:s}.img'/>
      <target dev='hda' bus='ide'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <disk type='file' device='cdrom'>
    <driver name='qemu'/>
      <source file='/var/lib/libvirt/iso/{image_file:s}' />
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
      <mac address='{macaddr:s}'/>
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
    <graphics type="vnc"  websocket="{websocketport:d}" passwd="{passwd:s}" listen="0.0.0.0"/>
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
</domain>""".format(hostname=hostname,
        uuid=uuid,
        memorysize=memorysize,
        cpu=cpu,
        image_file=image_file,
        macaddr=macaddr,
        websocketport=websocketport,
        passwd=passwd)


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
