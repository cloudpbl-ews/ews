import libvirt
import os
import time
import rrdtool
from django.conf import settings

hypervisor_url = "qemu+tls://" + settings.HYPERVISOR_URL + "/system"

statpath = "./static/statistics/data/"
cpurrdpath = statpath + "cpu/"
cpuusagepath = statpath + "cpuusage/"
cpupngpath= statpath + "cpupng/"
colors =["ff0000", "00ff00", "0000ff", "ffff00", "00ffff", "ff00ff"]

def rrd2plain():
    print "write to cpuuusage"
    files = os.listdir(cpurrdpath)
    for file in files:
        if(file == ".gitkeep"):
            continue
        os.system('rrdtool fetch '+ cpurrdpath + file + ' AVERAGE --start `date +%s`-600 |  sed -e \'1,3d\'  > ' +cpuusagepath + file.split('.')[0]+ "."+ file.split('.')[1]  +".txt" )


def rrd2png():
    print "write to cpupng"
    files = os.listdir(cpurrdpath)
    num_cpu = {}
    for file in files:
        if(file == ".gitkeep"):
            continue
        if file.split(".")[0] in num_cpu:
            num_cpu[file.split(".")[0]] += 1
        else:
            num_cpu[file.split(".")[0]] = 1
    print num_cpu
    for uuid, cpunum in num_cpu.iteritems():
        files = []
        endtime = time.time() - 10
        starttime = endtime - 3600
        for cpu in range(1, cpunum+1):
            files.append(cpurrdpath + uuid+"."+str(cpu)+".rrd")
        arg = []
        for i in range(len(files)):
            arg.append("DEF:s%d=%s:cpu:AVERAGE" % (i + 1, files[i]))
            arg.append("CDEF:s%d_per=s%d,100,*" % (i+1, i+1))
            arg.append("LINE:s%d_per#%s:cpu%d" % (i+1, colors[i%6],  i+1))

        rrdtool.graph(cpupngpath + uuid+".png",
                  "--imgformat=PNG",
                  "--start=%d" % starttime,
                  "--end=%d" % endtime,
                  "--height=380",
                  "--width=480",
                  "--title=cpu #%d" % (int(file.split(".")[-2])),
                  "--vertical-label=cpu utilization (%)",
                  "--upper-limit=100",
                  "--lower-limit=0",
                  "--rigid",
                  arg
                  );

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
