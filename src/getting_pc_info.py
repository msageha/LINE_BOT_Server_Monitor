import psutil
import subprocess
import time
import re

from notification import post_to_line
from message_dicts import notification_dict

def get_num(word):
    m = re.search(r'([0-9\.]+)', word)
    if m:
        return float(m.group())
    else:
        return 0

# 数値を小数点第1位で四捨五入して文字列に変換する
# def roundstr(size):
#     return str(round(size, 1))

# def bytesize_to_text(bytesize):
#     if bytesize < 1024:
#         return str(bytesize) + ' Bytes'
#     elif bytesize < 1024 ** 2:
#         return roundstr(bytesize / 1024.0) + ' KBytes'
#     elif bytesize < 1024 ** 3:
#         return roundstr(bytesize / (1024.0 ** 2)) + ' MBytes'
#     elif bytesize < 1024 ** 4:
#         return roundstr(bytesize / (1024.0 ** 3)) + ' GBytes'
#     elif bytesize < 1024 ** 5:
#         return roundstr(bytesize / (1024.0 ** 4)) + ' TBytes'
#     else:
#         return str(bytesize) + ' Bytes'

def measure_temp():
    stage = 3
    output = subprocess.getoutput('vcgencmd measure_temp')
    temp = get_num(output)
    if temp >= 60:
        stage = 3
    elif temp >= 40:
        stage = 2
    else:
        stage = 1
    return stage

def measure_volts():
    stage = 3
    output = subprocess.getoutput('vcgencmd measure_volts')
    volts = get_num(output)
    if volts > 1.5:
        stage = 3
    elif volts > 1.3:
        stage = 2
    else:
        stage = 1
    return stage

def cpu_used():
    stage = 3
    cpu_persent = psutil.cpu_percent()
    if cpu_persent >= 80:
        stage = 3
    elif cpu_persent >= 50:
        stage = 2
    else:
        stage = 1
    return stage

def memory_info():
    stage = 3
    mem = psutil.virtual_memory()
    mem_persent = mem.used / mem.total * 100
    if mem_persent >= 80:
        stage = 3
    elif mem_persent >= 50:
        stage = 2
    else:
        stage = 1
    return stage

def access():
    pass
    # net = psutil.net_connections()

if __name__=='__main__':
    cpu_stage = 0
    memory_stage = 0
    volts_stage = 0
    temp_stage = 0
    while True:
        message = ''
        tmp = cpu_used()
        if cpu_stage == 3 and tmp < 3:
            message = notification_dict['cpu']
        cpu_stage = tmp
        tmp = memory_info()
        if memory_stage == 3 and tmp < 3:
            message = notification_dict['memory']
        memory_stage = tmp
        tmp = measure_volts()
        if volts_stage < 3 and tmp == 3:
            message = notification_dict['volts']
        tmp = measure_temp()
        if temp_stage < 3 and tmp == 3:
            message = notification_dict['temp']
        if message:
            post_to_line(message=message)
        time.sleep(10)
