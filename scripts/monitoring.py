import statistics.stat as s
import time

def run():
    stat = s.StatCollector()
    i = 0
    while True:
        try:
            stat.UpdateVMlist()
            stat.CollectStat()
            if i == 0 or i % 6 ==0:
                s.rrd2plain()
            if i == 20 or i % 3600 == 0:
                s.rrd2png()
            time.sleep(1)
            if i >= 3600:
                i = 0
            i+=1
        except KeyboardInterrupt:
            break
        except Exception as e:
            print "Exception ", e
