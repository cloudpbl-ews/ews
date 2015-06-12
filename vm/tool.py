import sys
import os
import re
import random

def GenMac():
   mac = [ 0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff) ]
   return ':'.join(map(lambda x: "%02x" % x, mac))



def XMLGen(hostname,uuid,  memorysize, cpu, image_file, macaddr, websocketport, passwd ):
  print "<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>"
  print "  <name>%s</name>"   % hostname
  print "  <uuid>%s</uuid>  " % uuid
  print "  <memory unit='KiB'>%s</memory>" % memorysize
  print "  <currentMemory unit='KiB'>%s</currentMemory>" % memorysize
  print "  <vcpu placement='static'>%s</vcpu>" % cpu
  print "  <os>"
  print "    <type arch='x86_64' machine='pc-i440fx-1.7'>hvm</type>"
  print "    <boot dev='hd'/>"
  print "  </os>"
  print "  <features>"
  print "    <acpi/>"
  print "    <apic/>"
  print "    <pae/>"
  print "  </features>"
  print "  <clock offset='utc'/>"
  print "  <on_poweroff>destroy</on_poweroff>"
  print "  <on_reboot>restart</on_reboot>"
  print "  <on_crash>restart</on_crash>"
  print "  <devices>"
  print "  <emulator>/usr/bin/qemu-system-x86_64</emulator>"
  print "    <disk type='file' device='disk'>"
  print "      <driver name='qemu' type='raw'/>"
  print "      <source file='/var/lib/libvirt/images/%s'/>"  % image_file
  print "      <target dev='hda' bus='ide'/>"
  print "      <address type='drive' controller='0' bus='0' target='0' unit='0'/>"
  print "    </disk>"
  print "    <disk type='block' device='cdrom'>"
  print "      <driver name='qemu' type='raw'/>"
  print "      <target dev='hdc' bus='ide'/>"
  print "      <readonly/>"
  print "      <address type='drive' controller='0' bus='1' target='0' unit='0'/>"
  print "    </disk>"
  print "    <controller type='usb' index='0'>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>"
  print "    </controller>"
  print "    <controller type='pci' index='0' model='pci-root'/>"
  print "    <controller type='ide' index='0'>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>"
  print "    </controller>"
  print "    <interface type='bridge'>"
  print "      <mac address='%s'/>"  % macaddr
  print "      <source bridge='br0'/>"
  print "      <model type='e1000'/>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>"
  print "    </interface>"
  print "    <serial type='pty'>"
  print "      <target port='0'/>"
  print "    </serial>"
  print "    <console type='pty'>"
  print "      <target type='serial' port='0'/>"
  print "    </console>"
  print "    <input type='mouse' bus='ps2'/>"
  print "    <input type='keyboard' bus='ps2'/>"
  print "    <graphics type=\"vnc\"  websocket=\"%s\" passwd=\"%s\" listen=\"0.0.0.0\"/>" %(websocketport,  passwd)
  print "    <sound model='ich6'>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>"
  print "    </sound>"
  print "    <video>"
  print "      <model type='cirrus' vram='9216' heads='1'/>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>"
  print "    </video>"
  print "    <memballoon model='virtio'>"
  print "      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>"
  print "    </memballoon>"
  print "  </devices>"
  print "</domain>"
