import psutil
import subprocess
import time
import re

class Info:
    def __init__(self):
        pass

    def __call__(self):
        response = {}
        response['temp'] = self.measure_temp()
        response['volts'] = self.measure_volts()
        response['cpu'] = self.cpu_used()
        response['memory'] = self.memory_info()
        return response

    def get_num(self, word):
        m = re.search(r'([0-9\.]+)', word)
        if m:
            return float(m.group())
        else:
            return 0

    def measure_temp(self):
        output = subprocess.getoutput('vcgencmd measure_temp')
        temp = self.get_num(output)
        return str(temp)

    def measure_volts(self):
        output = subprocess.getoutput('vcgencmd measure_volts')
        volts = self.get_num(output)
        return str(volts)

    def cpu_used(self):
        cpu_persent = psutil.cpu_percent()
        return str(cpu_persent)

    def memory_info(self):
        mem = psutil.virtual_memory()
        mem_persent = mem.used / mem.total * 100
        return str(mem_persent)

    def access(self):
        pass
        # net = psutil.net_connections()
