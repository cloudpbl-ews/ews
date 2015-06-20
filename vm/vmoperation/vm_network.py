import libvirt
from uuid import UUID

from xml.dom import minidom # xml parcer module


# networks on the host
class HostNetwork():

	def __init__(self, uri):
		self.conn = libvirt.open(uri)

	# Return a list of VirtualNetwork objects
	def get_list_networks(self):
		vnw_list = []
		for vnw in self.conn.listAllNetworks():
			vnw_list.append( VirtualNetwork(vnw) )
		return vnw_list

class VirtualNetwork():

	def __init__(self, vnw):
		self.vnw = vnw

	def start(self):
		if not self.vnw.isActive():
			self.vnw.create()

	# this function needs privileged access
	def stop(self):
		if self.vnw.isActive():
			self.vnw.destroy()

	def delete(self):
		if not self.vnw.isActive():
			self.vnw.undefine()

	def is_auto(self):
		if self.vnw.autostart() == libvirt.VIR_CONNECT_LIST_NETWORKS_AUTOSTART:
			return True
		elif self.vnw.autostart() == libvirt.VIR_CONNECT_LIST_NETWORKS_NO_AUTOSTART:
			return False
		else:
			raise

	def name(self):
		return self.vnw.name()


# main() is for debug
if __name__ == '__main__':
	host_nw = HostNetwork("lxc:///")
	for vnw in host_nw.get_list_networks():
		print vnw.name()
