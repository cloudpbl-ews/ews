import libvirt
import os
import time
import rrdtool

hypervisor_url = "qemu+tls://157.82.3.111/system"

statpath = "../static/statistics/data/"
cpurrdpath = statpath + "cpu/"
cpuusagepath = statpath + "cpuusage/"

def rrd2plain():
  print "write to cpuuusage"
  files = os.listdir(cpurrdpath)
  for file in files:
    os.system('rrdtool fetch '+ cpurrdpath + file + ' AVERAGE --start `date +%s`-600 |  sed -e \'1,3d\'  > ' +cpuusagepath + file.split('.')[0]+ "."+ file.split('.')[1]  +".txt" )


def updateCpuRRD(uuid, idx, tm, util):
    fname = "%s/%s.%d.rrd" % (cpurrdpath, uuid, idx)
    print  uuid," -> ", util
    if not os.path.exists(fname):
        print "create rrd", uuid
        ## Create
        rrdtool.create(fname,
                       "--start=%d" % tm,
                       #"--step=300",
                       "--step=5",
                       #"DS:cpu:GAUGE:300:U:U",
                       "DS:cpu:GAUGE:5:U:U",
                       "RRA:AVERAGE:0.5:1:518400")
        return
    dstr = "%d:%f" % (tm, util)
    rrdtool.update(fname, dstr)


  
class StatCollector():
  def __init__(self):
    self.conn = libvirt.open(hypervisor_url)
    self.UpdateVMlist()
    self.cputimes = {}
    self.lastupdatecpu = {}

  def isConnectionAlive(self):
    try:
      self.conn.getHostname()
    except KeyboardInterrupt:
      raise
    except:
      return False
    return True


  def UpdateVMlist(self):
    self.vmlist = self.conn.listAllDomains()
    

  def CollectStat(self):
    self.UpdateVMlist()
    for vm in self.vmlist:
      curtime = time.time()
      vminfo = vm.info()
      uuid=vm.UUIDString()
      name=vm.name()
      id=vm.ID()
      state= vminfo[0]
      maxmem= vminfo[1]
      mem= vminfo[2]
      nvcpu= vminfo[3]
      cputime= vminfo[4]
      vcpus = {}
      if vm.ID() < 0:
         continue

      tvcpus = vm.vcpus()
      for i in range(nvcpu):
        affinity = ""
        for b in tvcpus[1][i]:
          if b:
            affinity += "y"
          else:
            affinity += "-"
        vcpus[tvcpus[0][i][0]+1] = {"state":tvcpus[0][i][1],
                                    "cputime":tvcpus[0][i][2],
                                    "cpu" : tvcpus[0][i][3],
                                    "affinity":affinity}

      for cpuid in range(nvcpu):
        cpuid += 1
        cpukey = "%s.%d" % (uuid, cpuid)
        if self.cputimes.has_key(cpukey):
          difftime = curtime - self.lastupdatecpu[cpukey]
          cptm = vcpus[cpuid]["cputime"] - self.cputimes[cpukey]
          cpuutil = 1.0 * cptm /1000000000/difftime
          print name
          updateCpuRRD(uuid, cpuid, curtime, cpuutil)
        self.cputimes[cpukey] = vcpus[cpuid]["cputime"]
        self.lastupdatecpu[cpukey] = curtime


if __name__ == "__main__":
  stat = StatCollector()
  i = 0
  while True:
    try:
      stat.UpdateVMlist()
      stat.CollectStat()
      if i > 5:
        rrd2plain()
        i=0
      time.sleep(1)
      i+=1
    except KeyboardInterrupt:
      break
    except Exception as e:
      print "Exception ", e
