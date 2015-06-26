import libvirt
from uuid import UUID

from xml.dom import minidom # xml parcer module
from xml.etree import ElementTree as ET


# CONSTANTS #
NETWORK_AUTOSTART = 1
NETWORK_NO_AUTOSTART = 0


# networks on the host
class HostVirtualNetworks():

    def __init__(self, uri):
        self.conn = libvirt.open(uri)

    # return a list of VirtualNetwork objects
    def get_list_networks(self):
        virt_nw_list = []
        for virt_nw in self.conn.listAllNetworks():
            virt_nw_list.append( VirtualNetwork(virt_nw) )
        return virt_nw_list

    def define_network_xml(self, net_xml):
        self.conn.networkCreateXML(net_xml)

    def create_network_xml(self, net_xml):
        self.conn.networkCreateXML(net_xml)

class VirtualNetwork():

    def __init__(self, virt_nw):
        self.virt_nw = virt_nw

    def start(self):
        if not self.virt_nw.isActive():
            self.virt_nw.create()
        else:
            raise Exception("Already Running")

    # this function needs privileged access
    def stop(self):
        if self.virt_nw.isActive():
            self.virt_nw.destroy()
        else:
            raise Exception("Already Stopping")

    def delete(self):
        if not self.virt_nw.isActive():
            self.virt_nw.undefine()
            self.virt_nw = None
        else:
            raise Exception("Not Stopping")

    def is_auto(self):
        if self.virt_nw.autostart() == 1: #
            return True
        else:
            return False

    # auto_val is NETWORK_AUTOSTART or NETWORK_NO_AUTOSTART
    def set_auto(self, auto_val):
        self.virt_nw.setAutostart(auto_val)


    def is_running(self):
        return self.virt_nw.isActive()

    # return the public name for that network. Example: default
    def name(self):
        return self.virt_nw.name()

    # return a bridge interface name to which a domain may connect a network interface in order to join the network. Example: br0
    def br_name(self):
        return self.virt_nw.bridgeName()

# net_name: the name of a virtual network, 
def gen_network_xml(net_name, br_name, ip_addr, net_mask, start_range, end_range):
    root = ET.Element('network')
    # set network's name
    name = ET.SubElement(root, 'name')
    name.text = net_name
    # set forward. Now fix nat
    forward = ET.SubElement(root, 'forward')
    forward.set('mode', 'nat')
    # set bridge name
    bridge = ET.SubElement(root, 'bridge')
    bridge.set('name', br_name)
    # set ip address and netmask
    ip = ET.SubElement(root, 'ip')
    ip.set('address', ip_addr)
    ip.set('netmask', net_mask)
    # set dhcp range
    dhcp = ET.SubElement(ip, 'dhcp')
    dhcp_range = ET.SubElement(dhcp, 'range')
    dhcp_range.set('start', start_range)
    dhcp_range.set('end', end_range)
    return ET.tostring(root)

        

# main() is for debug
if __name__ == '__main__':
    host_nw = HostVirtualNetworks("lxc:///")
    for nw in host_nw.get_list_networks():
        print nw.br_name(), nw.name()
        nw.set_auto(1)
