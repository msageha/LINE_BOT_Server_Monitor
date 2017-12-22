import psutil
import math


# 数値を小数点第1位で四捨五入して文字列に変換する
def roundstr(size):
    return str(round(size, 1))

def bytesize(bytesize):
    if bytesize < 1024:
        return str(bytesize) + ' Bytes'
    elif bytesize < 1024 ** 2:
        return roundstr(bytesize / 1024.0) + ' KBytes'
    elif bytesize < 1024 ** 3:
        return roundstr(bytesize / (1024.0 ** 2)) + ' MBytes'
    elif bytesize < 1024 ** 4:
        return roundstr(bytesize / (1024.0 ** 3)) + ' GBytes'
    elif bytesize < 1024 ** 5:
        return roundstr(bytesize / (1024.0 ** 4)) + ' TBytes'
    else:
        return str(bytesize) + ' Bytes'

def cpu():
    message = f'{psutil.cpu_percent()} % used'
    return message

def memory():
    mem = psutil.virtual_memory()
    used = bytesize(mem.used)
    total = bytesize(mem.total)
    message = f'{used} / {total}'
    return message

def access():
    pass
    # net = psutil.net_connections()
